"""
Descript-style video editor.
Transcript IS the edit. Select words -> Delete to cut. Playback skips cuts.
Run: python app.py [video_file]    ->    http://localhost:3028
"""
import os, sys, json, subprocess, tempfile, threading, struct
from pathlib import Path
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# ─── State ───────────────────────────────────────────────────────────────────
S = {
    "video_path": None,
    "duration":   0.0,
    "words":      [],     # [{start, end, word}]
    "deleted":    [],     # [bool] parallel to words — True = cut from video
    "output_dir": None,
    "volume":     3.0,
    "peaks":      None,
    "transcribing": False,
    "transcribe_msg": "",
    "rendering":  False,
    "render_log": [],
}

def get_dur(path):
    r = subprocess.run(
        ["ffprobe","-v","quiet","-print_format","json","-show_format",path],
        capture_output=True, text=True, timeout=15)
    return float(json.loads(r.stdout)["format"]["duration"])

# ─── Video streaming ──────────────────────────────────────────────────────────
@app.route("/video")
def video():
    p = S["video_path"]
    if not p or not os.path.exists(p): return "No video", 404
    size = os.path.getsize(p)
    rh = request.headers.get("Range","")
    s, e = 0, size-1
    if rh:
        pts = rh.replace("bytes=","").split("-")
        s = int(pts[0]) if pts[0] else 0
        e = int(pts[1]) if len(pts)>1 and pts[1].strip() else size-1
    with open(p,"rb") as f:
        f.seek(s); data = f.read(e-s+1)
    return Response(data, status=206 if rh else 200, headers={
        "Content-Range":f"bytes {s}-{e}/{size}",
        "Accept-Ranges":"bytes","Content-Length":str(e-s+1),"Content-Type":"video/mp4"})

# ─── API ──────────────────────────────────────────────────────────────────────
@app.route("/api/state")
def state():
    kept = sum(1 for i,w in enumerate(S["words"]) if not S["deleted"][i]) if S["words"] else 0
    total_kept = sum(
        S["words"][i]["end"]-S["words"][i]["start"]
        for i in range(len(S["words"])) if not S["deleted"][i]
    ) if S["words"] else 0.0
    return jsonify({
        "video_path": S["video_path"],
        "duration":   S["duration"],
        "words_count": len(S["words"]),
        "deleted_count": sum(S["deleted"]) if S["deleted"] else 0,
        "kept_words": kept,
        "kept_seconds": round(total_kept, 2),
        "volume": S["volume"],
        "transcribing": S["transcribing"],
        "transcribe_msg": S["transcribe_msg"],
        "rendering": S["rendering"],
        "output_dir": S["output_dir"],
        "has_peaks": S["peaks"] is not None,
    })

@app.route("/api/load", methods=["POST"])
def load():
    path = (request.json or {}).get("path","").strip()
    if not path or not os.path.exists(path):
        return jsonify({"error": f"Not found: {path}"}), 400
    try:   dur = get_dur(path)
    except: dur = 0.0
    S.update({"video_path":path,"duration":dur,"words":[],"deleted":[],
               "output_dir":str(Path(path).parent),"peaks":None})
    return jsonify({"ok":True,"duration":dur})

@app.route("/api/waveform")
def waveform():
    if S["peaks"] is not None: return jsonify({"peaks":S["peaks"]})
    p = S["video_path"]
    if not p: return jsonify({"peaks":[]})
    try:
        dur = S["duration"] or 60
        sr = max(200, min(8000, int(4000/dur)+1))
        r = subprocess.run(["ffmpeg","-i",p,"-ac","1","-ar",str(sr),"-f","f32le","-"],
                           capture_output=True, timeout=120)
        n = len(r.stdout)//4
        if not n: return jsonify({"peaks":[]})
        samp = struct.unpack(f"{n}f", r.stdout)
        chunk = max(1, n//3000)
        peaks = [round(max(abs(x) for x in samp[i:i+chunk]),4) for i in range(0,n,chunk)]
        mx = max(peaks) if peaks else 1
        if mx > 0: peaks = [v/mx for v in peaks]
        S["peaks"] = peaks
        return jsonify({"peaks":peaks})
    except Exception as ex:
        return jsonify({"peaks":[],"error":str(ex)})

@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    if S["transcribing"]: return jsonify({"error":"Already running"}), 400
    p = S["video_path"]
    if not p: return jsonify({"error":"No video"}), 400
    model_size = (request.json or {}).get("model","base")
    def run():
        S["transcribing"]=True; S["transcribe_msg"]="Loading Whisper…"
        try:
            import whisper
            m = whisper.load_model(model_size)
            S["transcribe_msg"]="Transcribing…"
            res = m.transcribe(p, word_timestamps=True)
            words=[]
            for seg in res["segments"]:
                for w in seg.get("words",[]):
                    words.append({"start":round(w["start"],3),
                                  "end":round(w["end"],3),
                                  "word":w["word"].strip()})
            S["words"]=words
            S["deleted"]=[False]*len(words)
            S["transcribe_msg"]=f"Done — {len(words)} words"
        except Exception as ex:
            S["transcribe_msg"]=f"Error: {ex}"
        finally:
            S["transcribing"]=False
    threading.Thread(target=run, daemon=True).start()
    return jsonify({"ok":True})

@app.route("/api/words")
def words_api():
    return jsonify({"words": S["words"], "deleted": S["deleted"]})

@app.route("/api/set-deleted", methods=["POST"])
def set_deleted():
    d = request.json.get("deleted",[])
    if len(d) == len(S["words"]):
        S["deleted"] = [bool(x) for x in d]
    return jsonify({"ok":True})

@app.route("/api/auto-edit", methods=["POST"])
def auto_edit():
    words = S["words"]
    if not words: return jsonify({"error":"Transcribe first"}), 400
    deleted = [False]*len(words)
    FILLERS = {"um","uh","hmm","uhh","umm","hm","ugh","mhm","mmm"}
    TAKE_GAP = 2.5

    # 1. Filler words
    for i,w in enumerate(words):
        if w["word"].lower().strip(",.!?-—") in FILLERS:
            deleted[i] = True

    # 2. Consecutive duplicates (stutters)
    for i in range(len(words)-1):
        t1 = words[i]["word"].lower().strip(",.!?-—")
        t2 = words[i+1]["word"].lower().strip(",.!?-—")
        if t1==t2 and len(t1)>1 and words[i+1]["start"]-words[i]["end"] < 0.5:
            deleted[i] = True

    # 3. Find takes (>TAKE_GAP silence) — mark short takes as deleted
    takes, ts = [], 0
    for i in range(1, len(words)):
        if words[i]["start"]-words[i-1]["end"] >= TAKE_GAP:
            takes.append((ts, i-1)); ts=i
    takes.append((ts, len(words)-1))
    # Short takes that aren't the last one = likely false starts
    for j,(ti,tj) in enumerate(takes[:-1]):
        if tj-ti+1 <= 5:
            for k in range(ti,tj+1): deleted[k]=True

    # 4. Within-take hesitation gaps (>0.9s pause mid-speech)
    take_bdy = {words[ti]["start"] for ti,_ in takes if ti>0}
    for i in range(len(words)-1):
        g = words[i+1]["start"]-words[i]["end"]
        if g > 0.9 and g < TAKE_GAP and words[i]["end"] not in take_bdy:
            # Mark the words immediately around the gap - don't delete them,
            # but mark the word BEFORE the gap if it looks like a restart
            # (heuristic: if the word is a function word at end of incomplete phrase)
            pass  # conservative: don't delete around gaps automatically

    S["deleted"] = deleted
    n_del = sum(deleted)
    kept_sec = sum(words[i]["end"]-words[i]["start"] for i in range(len(words)) if not deleted[i])
    return jsonify({"deleted": deleted, "n_deleted": n_del,
                    "n_takes": len(takes), "kept_sec": round(kept_sec,2)})

@app.route("/api/volume", methods=["POST"])
def volume():
    S["volume"] = float((request.json or {}).get("volume",3.0))
    return jsonify({"ok":True})

@app.route("/api/render", methods=["POST"])
def render():
    if S["rendering"]: return jsonify({"error":"Already rendering"}), 400
    data = request.json or {}
    words = S["words"]; deleted = S["deleted"]
    if not words: return jsonify({"error":"No transcript"}), 400

    # Build clips from non-deleted word runs
    clips=[]
    in_clip=False; cs=0; ce=0
    PAD=0.05
    for i,w in enumerate(words):
        if not deleted[i]:
            if not in_clip: cs=max(0,w["start"]-PAD); in_clip=True
            ce=w["end"]+PAD
        else:
            if in_clip: clips.append((round(cs,3),round(ce,3))); in_clip=False
    if in_clip: clips.append((round(cs,3),round(min(ce,S["duration"]),3)))

    if not clips: return jsonify({"error":"Everything is deleted"}), 400

    out_name = data.get("output_name","output.mp4")
    out_dir  = data.get("output_dir", S["output_dir"]) or S["output_dir"]
    out_path = str(Path(out_dir)/out_name)
    source   = S["video_path"]; vol=S["volume"]

    def run():
        S["rendering"]=True; S["render_log"]=["Starting render…"]
        clip_dir=tempfile.mkdtemp(prefix="dsc_")
        try:
            files=[]
            for i,(cs,ce) in enumerate(clips):
                out=os.path.join(clip_dir,f"c{i:04d}.mp4")
                r=subprocess.run(["ffmpeg","-y","-i",source,
                    "-ss",str(cs),"-to",str(ce),
                    "-c:v","libx264","-crf","18","-preset","fast",
                    "-c:a","aac","-b:a","192k","-avoid_negative_ts","make_zero",out],
                    capture_output=True,text=True,timeout=300)
                if r.returncode!=0:
                    S["render_log"].append(f"[ERR] clip {i+1}: {r.stderr[-200:]}"); return
                files.append(out)
                S["render_log"].append(f"OK {i+1}/{len(clips)} ({ce-cs:.1f}s)")
            concat=os.path.join(clip_dir,"c.txt")
            with open(concat,"w") as f:
                for p in files: f.write(f"file '{p}'\n")
            S["render_log"].append("Joining + boosting volume…")
            r=subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",concat,
                "-af",f"volume={vol}","-c:v","copy",out_path],
                capture_output=True,text=True,timeout=600)
            if r.returncode!=0: S["render_log"].append(f"[ERR] {r.stderr[-200:]}")
            else: S["render_log"].append(f"Done -> {out_path}")
        except Exception as ex: S["render_log"].append(f"[EXC] {ex}")
        finally: S["rendering"]=False

    threading.Thread(target=run,daemon=True).start()
    return jsonify({"ok":True,"clips_count":len(clips),"output":out_path})

@app.route("/api/render/log")
def render_log(): return jsonify({"rendering":S["rendering"],"log":S["render_log"]})

# ─── UI ───────────────────────────────────────────────────────────────────────
UI = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Editor</title>
<style>
*, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
:root {
  --bg:     #111;
  --surf:   #161616;
  --surf2:  #1c1c1c;
  --border: #252525;
  --bd2:    #2e2e2e;
  --txt:    #d4d4d4;
  --txt2:   #666;
  --txt3:   #3a3a3a;
  --blue:   #1d4ed8;
  --blue-l: #3b82f6;
  --green:  #16a34a;
  --green-l:#4ade80;
  --red:    #dc2626;
  --yellow: #ca8a04;
  --accent: #3b82f6;
}
html,body { height:100%; overflow:hidden; background:var(--bg); color:var(--txt);
  font:13px/1.5 "SF Pro Display","Segoe UI",system-ui,sans-serif; }

/* ─── Shell ─────────────────────────────────────────────────────── */
#shell { display:grid; grid-template-rows:46px 1fr 28px; height:100vh; }

/* ─── Header ──────────────────────────────────────────────────────  */
#hdr { background:var(--surf); border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:6px; padding:0 14px; }
#hdr .brand { font-size:11px; font-weight:600; letter-spacing:2px; color:var(--txt2);
  text-transform:uppercase; margin-right:10px; }
.sep { width:1px; height:20px; background:var(--border); margin:0 3px; }
button { font:12px/1 "SF Pro Display","Segoe UI",system-ui,sans-serif;
  background:var(--surf2); border:1px solid var(--bd2); color:var(--txt);
  padding:5px 12px; border-radius:4px; cursor:pointer; transition:background .12s,border-color .12s; }
button:hover { background:#232323; border-color:#3a3a3a; }
button:disabled { opacity:.35; cursor:default; }
button.primary { background:#1e3a6a; border-color:var(--blue-l); color:#93c5fd; }
button.primary:hover { background:#254a80; }
button.ghost { background:transparent; border-color:transparent; color:var(--txt2); }
button.ghost:hover { background:var(--surf2); border-color:var(--bd2); color:var(--txt); }
#hdr-right { margin-left:auto; display:flex; align-items:center; gap:6px; }
#hdr-status { font-size:11px; color:var(--txt2); }

/* ─── Main ────────────────────────────────────────────────────────  */
#main { display:grid; grid-template-columns:1fr 300px; overflow:hidden; }

/* ─── Transcript ──────────────────────────────────────────────────  */
#tx-wrap { display:flex; flex-direction:column; border-right:1px solid var(--border); overflow:hidden; }
#tx-toolbar { flex-shrink:0; display:flex; gap:6px; padding:8px 16px;
  border-bottom:1px solid var(--border); background:var(--surf); }
#tx-toolbar span { font-size:11px; color:var(--txt2); align-self:center; margin-left:auto; }
#tx-scroll { flex:1; overflow-y:auto; padding:32px 48px; }
#tx { font-size:16px; line-height:2.2; color:var(--txt); outline:none; }
/* words */
.w { display:inline; padding:1px 1px; border-radius:2px; cursor:text;
  transition:background .08s; white-space:pre-wrap; }
.w:hover { background:#1e1e1e; }
.w.del { color:var(--txt3); text-decoration:line-through; text-decoration-color:#333; }
.w.sel { background:#1e3a5f; color:#93c5fd; border-radius:2px; }
.w.sel.del { background:#3a1a1a; color:#555; text-decoration:line-through; }
.w.playing { background:#1a2e1a; color:var(--green-l); border-radius:2px; }
/* take break */
.take-sep { display:block; margin:12px 0 8px; border:none;
  border-top:1px solid var(--border); opacity:.5; }

/* ─── Right panel ─────────────────────────────────────────────────  */
#rp { display:flex; flex-direction:column; background:var(--surf); overflow:hidden; }

/* video */
#vid-wrap { background:#000; flex-shrink:0; position:relative; }
video { width:100%; display:block; max-height:195px; object-fit:contain; }
#vid-overlay { position:absolute; inset:0; display:flex; align-items:center;
  justify-content:center; pointer-events:none; }
#vid-overlay span { font-size:11px; color:#444; text-align:center; padding:20px; }

/* transport */
#transport { display:flex; align-items:center; justify-content:center; gap:4px;
  padding:8px; border-bottom:1px solid var(--border); flex-shrink:0; }
#transport button { padding:4px 12px; font-size:14px; }
#timecode { text-align:center; font:12px/1.8 "JetBrains Mono","Consolas",monospace;
  color:var(--txt2); padding:0 12px 6px; border-bottom:1px solid var(--border); flex-shrink:0; }
#timecode span { color:var(--txt); }

/* waveform */
#wv-wrap { padding:8px 12px 4px; border-bottom:1px solid var(--border); flex-shrink:0; }
#wv-label { font-size:10px; color:var(--txt3); text-transform:uppercase;
  letter-spacing:1px; margin-bottom:4px; }
canvas#wv { width:100%; height:36px; display:block; border-radius:3px;
  background:#0d0d0d; cursor:pointer; }

/* actions */
#actions { padding:10px 12px; display:flex; flex-direction:column; gap:5px; flex-shrink:0;
  border-bottom:1px solid var(--border); }
#actions .section-label { font-size:10px; color:var(--txt3); text-transform:uppercase;
  letter-spacing:1px; margin-bottom:2px; }
#actions button { text-align:left; padding:6px 10px; font-size:12px; }

/* vol */
#vol-row { display:flex; align-items:center; gap:8px; padding:10px 12px;
  border-bottom:1px solid var(--border); flex-shrink:0; }
#vol-row label { font-size:11px; color:var(--txt2); }
#vol-in { width:64px; background:#0d0d0d; border:1px solid var(--bd2); color:var(--txt);
  padding:4px 8px; border-radius:3px; font:12px "JetBrains Mono","Consolas",monospace; }

/* load input */
#load-row { display:flex; gap:6px; padding:10px 12px; border-bottom:1px solid var(--border);
  flex-shrink:0; }
#load-row input { flex:1; background:#0d0d0d; border:1px solid var(--bd2); color:var(--txt);
  padding:4px 8px; border-radius:3px; font:11px "JetBrains Mono","Consolas",monospace; }
#load-row input::placeholder { color:var(--txt3); }

/* render status */
#rp-log { flex:1; overflow-y:auto; padding:8px 12px; font:11px "JetBrains Mono",monospace;
  color:var(--txt2); }
#rp-log .ok  { color:#4ade80; }
#rp-log .err { color:#f87171; }

/* ─── Status bar ──────────────────────────────────────────────────  */
#sb { background:#0d0d0d; border-top:1px solid var(--border);
  display:flex; align-items:center; gap:16px; padding:0 14px;
  font-size:11px; color:var(--txt2); overflow:hidden; }
#sb code { font-family:"JetBrains Mono","Consolas",monospace; color:var(--txt); }

/* scrollbar */
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--bd2); border-radius:3px; }
</style>
</head>
<body>
<div id="shell">

<!-- Header -->
<header id="hdr">
  <div class="brand">Edit</div>
  <button class="ghost" onclick="triggerLoad()">Load file</button>
  <button id="btn-tx" onclick="doTranscribe()">Transcribe</button>
  <div class="sep"></div>
  <button onclick="doAutoEdit()" id="btn-auto">Auto-edit</button>
  <button class="ghost" onclick="removeFillers()">Remove fillers</button>
  <div class="sep"></div>
  <button class="ghost" onclick="doUndo()" title="Ctrl+Z">↩ Undo</button>
  <button class="ghost" onclick="doRedo()" title="Ctrl+Shift+Z">↺ Redo</button>
  <div id="hdr-right">
    <span id="hdr-status"></span>
    <button class="primary" onclick="showRender()">Export ▸</button>
  </div>
</header>

<!-- Main -->
<div id="main">

  <!-- Transcript -->
  <div id="tx-wrap">
    <div id="tx-toolbar">
      <button class="ghost" style="font-size:11px;padding:3px 8px" onclick="restoreAll()">Restore all</button>
      <button class="ghost" style="font-size:11px;padding:3px 8px" onclick="deleteAll()">Delete all</button>
      <span id="sel-hint">Click to seek · Select words then Delete to cut</span>
    </div>
    <div id="tx-scroll">
      <div id="tx">
        <span style="color:#333;font-size:14px">Load a video, then click Transcribe.<br><br>
        Select words and press <kbd style="background:#1e1e1e;padding:1px 6px;border-radius:3px;font-size:12px">Delete</kbd> to cut them from the video.
        <br>Deleted words show as <span style="text-decoration:line-through;color:#333">strikethrough</span>.
        Playback skips them automatically.</span>
      </div>
    </div>
  </div>

  <!-- Right -->
  <div id="rp">
    <div id="load-row">
      <input type="text" id="vpath" placeholder="Video file path…" onkeydown="if(event.key==='Enter')doLoad()">
      <button onclick="doLoad()">Open</button>
    </div>
    <div id="vid-wrap">
      <video id="player" preload="metadata"></video>
    </div>
    <div id="transport">
      <button onclick="step(-10)" title="J">⏮ 10s</button>
      <button onclick="togglePlay()" id="btn-play">▶</button>
      <button onclick="step(10)" title="L">10s ⏭</button>
    </div>
    <div id="timecode"><span id="tc-cur">00:00.000</span> / <span id="tc-tot">00:00.000</span></div>

    <div id="wv-wrap">
      <div id="wv-label">Overview</div>
      <canvas id="wv"></canvas>
    </div>

    <div id="actions">
      <div class="section-label">Quick edits</div>
      <button onclick="removeFillers()">Remove um / uh / hmm</button>
      <button onclick="removeFalseStarts()">Remove false starts (short takes)</button>
      <button onclick="restoreAll()">Restore everything</button>
    </div>

    <div id="vol-row">
      <label>Volume boost</label>
      <input type="number" id="vol-in" value="3.0" step="0.5" min="0.5" max="20"
        onchange="setVol(this.value)"> ×
    </div>

    <div id="rp-log"><span style="color:#2a2a2a">Render log will appear here.</span></div>
  </div>

</div>

<!-- Status bar -->
<div id="sb">
  <span id="sb-cuts">—</span>
  <span id="sb-kept">—</span>
  <span id="sb-vol">Vol 3.0×</span>
  <div style="flex:1"></div>
  <span id="sb-msg" style="color:#3a3a3a"></span>
</div>

</div><!-- shell -->

<!-- Render dialog -->
<div id="dlg" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:99;align-items:center;justify-content:center;">
  <div style="background:#1c1c1c;border:1px solid #333;border-radius:8px;padding:24px;width:420px;">
    <h2 style="font-size:14px;margin-bottom:16px;color:#d4d4d4">Export</h2>
    <div style="display:flex;flex-direction:column;gap:10px;">
      <div>
        <label style="font-size:11px;color:#666;display:block;margin-bottom:4px">Filename</label>
        <input type="text" id="dlg-name" value="output.mp4"
          style="width:100%;background:#111;border:1px solid #333;color:#d4d4d4;padding:6px 10px;border-radius:4px;font:13px monospace">
      </div>
      <div>
        <label style="font-size:11px;color:#666;display:block;margin-bottom:4px">Destination folder</label>
        <input type="text" id="dlg-dir"
          style="width:100%;background:#111;border:1px solid #333;color:#666;padding:6px 10px;border-radius:4px;font:11px monospace">
      </div>
    </div>
    <div style="display:flex;gap:8px;margin-top:16px">
      <button class="primary" onclick="doRender()">Export</button>
      <button onclick="closeDlg()">Cancel</button>
    </div>
  </div>
</div>

<script>
'use strict';
// ─── State ────────────────────────────────────────────────────────────────────
const player = document.getElementById('player');
let words    = [];     // [{start,end,word}]
let deleted  = [];     // [bool]
let dur      = 0;
let peaks    = [];

// Selection state
let selAnchor = -1, selHead = -1, isSelecting = false;

// Undo stack — array of deleted[] snapshots
let undoStack = [], redoStack = [];

// ─── Utilities ────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const api = async (url, body) => {
  const opts = body !== undefined
    ? {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}
    : {};
  return (await fetch(url, opts)).json();
};
const fmt = t => {
  const m = Math.floor(t/60), s = t%60;
  return `${String(m).padStart(2,'0')}:${s.toFixed(3).padStart(6,'0')}`;
};

// ─── Load ─────────────────────────────────────────────────────────────────────
function triggerLoad() { $('vpath').focus(); }

async function doLoad() {
  const path = $('vpath').value.trim();
  if (!path) return;
  const d = await api('/api/load', {path});
  if (d.error) { alert(d.error); return; }
  dur = d.duration;
  $('tc-tot').textContent = fmt(dur);
  player.src = '/video?t='+Date.now(); player.load();
  $('dlg-dir').value = '';
  const st = await api('/api/state');
  $('dlg-dir').value = st.output_dir || '';
  words=[]; deleted=[];
  renderTranscript();
  loadWaveform();
}

// ─── Waveform ─────────────────────────────────────────────────────────────────
async function loadWaveform() {
  const d = await api('/api/waveform');
  if (d.peaks && d.peaks.length) { peaks = d.peaks; drawWaveform(); }
}

function drawWaveform() {
  const cv = $('wv');
  const W = cv.offsetWidth * devicePixelRatio;
  const H = cv.offsetHeight * devicePixelRatio;
  cv.width=W; cv.height=H;
  const ctx = cv.getContext('2d');
  ctx.clearRect(0,0,W,H);
  if (!peaks.length) return;

  // grey base
  for (let px=0; px<W; px++) {
    const pi = Math.floor(px/W*peaks.length);
    const amp = (peaks[pi]||0)*H*0.8;
    ctx.fillStyle='#1a1a1a';
    ctx.fillRect(px,(H-amp)/2,1,Math.max(1,amp));
  }
  // colour by keep/delete
  if (!words.length) return;
  for (let px=0; px<W; px++) {
    const t = (px/W)*dur;
    // find word at this time
    const wi = words.findIndex(w => t>=w.start && t<w.end);
    const col = wi>=0 ? (deleted[wi] ? '#3a1a1a' : '#1e3a6a') : '#1a1a1a';
    const pi = Math.floor(px/W*peaks.length);
    const amp = (peaks[pi]||0)*H*0.8;
    ctx.fillStyle=col;
    ctx.fillRect(px,(H-amp)/2,1,Math.max(1,amp));
  }
  // playhead
  if (dur>0) {
    const px = Math.floor((player.currentTime/dur)*W);
    ctx.fillStyle='#ef4444';
    ctx.fillRect(px,0,1,H);
  }
}

// click waveform → seek
$('wv').addEventListener('click', e => {
  if (!dur) return;
  const r = $('wv').getBoundingClientRect();
  const t = ((e.clientX-r.left)/r.width)*dur;
  seekToKept(t);
});

function seekToKept(t) {
  // If t lands in a deleted region, jump to next kept word
  for (let i=0; i<words.length; i++) {
    if (!deleted[i] && words[i].end > t) {
      player.currentTime = Math.max(t, words[i].start);
      return;
    }
  }
}

// ─── Transcribe ───────────────────────────────────────────────────────────────
async function doTranscribe() {
  const btn = $('btn-tx');
  btn.disabled=true; btn.textContent='Transcribing…';
  await api('/api/transcribe', {model:'base'});
  pollTx(btn);
}

async function pollTx(btn) {
  const st = await api('/api/state');
  $('hdr-status').textContent = st.transcribe_msg;
  if (st.transcribing) { setTimeout(()=>pollTx(btn),1500); return; }
  const d = await api('/api/words');
  words = d.words; deleted = d.deleted;
  undoStack=[]; redoStack=[];
  btn.disabled=false; btn.textContent='Transcribe';
  renderTranscript();
  updateStatus();
}

// ─── Transcript rendering ─────────────────────────────────────────────────────
function renderTranscript() {
  const tx = $('tx');
  if (!words.length) return;
  tx.innerHTML='';
  words.forEach((w,i) => {
    // Take break
    if (i>0 && w.start-words[i-1].end > 2.5) {
      const hr = document.createElement('hr');
      hr.className='take-sep'; tx.appendChild(hr);
    }
    const span = document.createElement('span');
    span.className = 'w' + (deleted[i]?' del':'');
    span.dataset.i = i;
    span.textContent = w.word + ' ';
    span.addEventListener('mousedown', wordMouseDown);
    span.addEventListener('mouseenter', wordMouseEnter);
    tx.appendChild(span);
  });
}

function wordMouseDown(e) {
  const i = parseInt(this.dataset.i);
  if (e.shiftKey && selAnchor>=0) {
    // extend selection
    selHead = i;
    applySelectionVis();
    e.preventDefault(); return;
  }
  // Start new selection
  selAnchor = i; selHead = i; isSelecting = true;
  applySelectionVis();
  // Seek video to this word
  if (!deleted[i]) player.currentTime = words[i].start;
  else {
    // find next non-deleted word near this position
    for (let j=i; j<words.length; j++) { if (!deleted[j]){player.currentTime=words[j].start;break;} }
  }
  e.preventDefault();
}

function wordMouseEnter(e) {
  if (!isSelecting) return;
  selHead = parseInt(this.dataset.i);
  applySelectionVis();
}

document.addEventListener('mouseup', () => { isSelecting=false; });

function applySelectionVis() {
  const lo=Math.min(selAnchor,selHead), hi=Math.max(selAnchor,selHead);
  document.querySelectorAll('.w').forEach((el,i) => {
    el.classList.toggle('sel', i>=lo && i<=hi);
  });
  updateSelHint(hi-lo+1);
}

function clearSelection() {
  selAnchor=-1; selHead=-1;
  document.querySelectorAll('.w.sel').forEach(el=>el.classList.remove('sel'));
  $('sel-hint').textContent='Click to seek · Select words then Delete to cut';
}

function updateSelHint(n) {
  if (n<=0) { $('sel-hint').textContent='Click to seek · Select words then Delete to cut'; return; }
  const secs = words.slice(Math.min(selAnchor,selHead), Math.max(selAnchor,selHead)+1)
    .reduce((a,w)=>a+w.end-w.start,0);
  $('sel-hint').textContent=`${n} word${n>1?'s':''} selected (${secs.toFixed(1)}s) — press Delete to cut`;
}

// Apply deleted[] state to DOM word spans
function applyDeleted() {
  document.querySelectorAll('.w').forEach((el,i) => {
    el.classList.toggle('del', !!deleted[i]);
  });
  drawWaveform();
  updateStatus();
}

// ─── Delete / Restore ────────────────────────────────────────────────────────
function cutSelection() {
  if (selAnchor<0) return;
  const lo=Math.min(selAnchor,selHead), hi=Math.max(selAnchor,selHead);
  pushUndo();
  for (let i=lo;i<=hi;i++) deleted[i]=true;
  clearSelection();
  applyDeleted();
  saveDeleted();
}

function restoreSelection() {
  if (selAnchor<0) return;
  const lo=Math.min(selAnchor,selHead), hi=Math.max(selAnchor,selHead);
  pushUndo();
  for (let i=lo;i<=hi;i++) deleted[i]=false;
  clearSelection();
  applyDeleted();
  saveDeleted();
}

function restoreAll() {
  pushUndo(); deleted=deleted.map(()=>false);
  applyDeleted(); saveDeleted();
}
function deleteAll() {
  pushUndo(); deleted=deleted.map(()=>true);
  applyDeleted(); saveDeleted();
}

// ─── Quick edits ─────────────────────────────────────────────────────────────
function removeFillers() {
  if (!words.length) return;
  const FILLERS=new Set(["um","uh","hmm","uhh","umm","hm","ugh","mhm","mmm"]);
  pushUndo();
  words.forEach((w,i)=>{
    if (FILLERS.has(w.word.toLowerCase().replace(/[,.!?—\-]/g,''))) deleted[i]=true;
  });
  applyDeleted(); saveDeleted();
}

function removeFalseStarts() {
  if (!words.length) return;
  pushUndo();
  // Find takes (>2.5s gaps), delete short ones (<=5 words) that aren't the last
  let takes=[], ts=0;
  for (let i=1;i<words.length;i++) {
    if (words[i].start-words[i-1].end>=2.5){takes.push([ts,i-1]);ts=i;}
  }
  takes.push([ts,words.length-1]);
  for (let j=0;j<takes.length-1;j++){
    const [ti,tj]=takes[j];
    if (tj-ti+1<=5) for(let k=ti;k<=tj;k++) deleted[k]=true;
  }
  applyDeleted(); saveDeleted();
}

async function doAutoEdit() {
  const btn=$('btn-auto');
  btn.disabled=true; btn.textContent='Analysing…';
  const d = await api('/api/auto-edit',{});
  btn.disabled=false; btn.textContent='Auto-edit';
  if (d.error){alert(d.error);return;}
  pushUndo();
  deleted = d.deleted;
  applyDeleted(); saveDeleted();
  $('hdr-status').textContent=`Auto: ${d.n_takes} takes · ${d.n_deleted} words cut · ${d.kept_sec}s kept`;
}

// ─── Undo / Redo ─────────────────────────────────────────────────────────────
function pushUndo() {
  undoStack.push([...deleted]);
  redoStack=[];
  if (undoStack.length>80) undoStack.shift();
}

function doUndo() {
  if (!undoStack.length) return;
  redoStack.push([...deleted]);
  deleted = undoStack.pop();
  applyDeleted(); saveDeleted();
}

function doRedo() {
  if (!redoStack.length) return;
  undoStack.push([...deleted]);
  deleted = redoStack.pop();
  applyDeleted(); saveDeleted();
}

async function saveDeleted() {
  await api('/api/set-deleted',{deleted});
}

// ─── Playback ─────────────────────────────────────────────────────────────────
player.addEventListener('play',  ()=>{ $('btn-play').textContent='⏸'; });
player.addEventListener('pause', ()=>{ $('btn-play').textContent='▶'; });
player.addEventListener('loadedmetadata', ()=>{
  dur=player.duration; $('tc-tot').textContent=fmt(dur);
});

let lastSkipAt = -1;
player.addEventListener('timeupdate', ()=>{
  const t = player.currentTime;
  $('tc-cur').textContent = fmt(t);
  drawWaveform(); // update playhead
  highlightWord(t);

  // Skip deleted regions
  if (!words.length) return;
  // find if we're in a deleted word
  const wi = words.findIndex(w => t>=w.start && t<w.end);
  if (wi>=0 && deleted[wi] && Math.abs(t-lastSkipAt)>0.3) {
    // Find next non-deleted word
    const next = words.slice(wi+1).find((w,j) => !deleted[wi+1+j]);
    if (next) { lastSkipAt=t; player.currentTime=next.start; }
    else { player.pause(); }
  }
});

function highlightWord(t) {
  document.querySelectorAll('.w.playing').forEach(el=>el.classList.remove('playing'));
  const wi = words.findIndex(w => t>=w.start && t<=w.end);
  if (wi<0) return;
  const el = document.querySelectorAll('.w')[wi];
  if (el && !el.classList.contains('sel')) {
    el.classList.add('playing');
    el.scrollIntoView({block:'nearest',behavior:'smooth'});
  }
}

function togglePlay() {
  if (player.paused) player.play(); else player.pause();
}
function step(s) {
  player.currentTime = Math.max(0,Math.min(dur,player.currentTime+s));
}

// ─── Volume ───────────────────────────────────────────────────────────────────
async function setVol(v) {
  await api('/api/volume',{volume:parseFloat(v)});
  $('sb-vol').textContent=`Vol ${parseFloat(v).toFixed(1)}x`;
}

// ─── Status ────────────────────────────────────────────────────────────────────
function updateStatus() {
  const nDel = deleted.filter(Boolean).length;
  const kept = words.reduce((a,w,i)=>a+(deleted[i]?0:w.end-w.start),0);
  const total = words.reduce((a,w)=>a+w.end-w.start,0);
  $('sb-cuts').textContent = nDel > 0 ? `${nDel} word${nDel>1?'s':''} cut` : 'No cuts';
  $('sb-kept').textContent = words.length ? `${kept.toFixed(1)}s of ${total.toFixed(1)}s kept` : '—';
}

// ─── Render ───────────────────────────────────────────────────────────────────
function showRender() { $('dlg').style.display='flex'; }
function closeDlg()   { $('dlg').style.display='none'; }
$('dlg').addEventListener('click', e=>{ if(e.target===$('dlg')) closeDlg(); });

async function doRender() {
  const btn = $('dlg').querySelector('button.primary');
  btn.disabled=true; btn.textContent='Exporting…';
  const d = await api('/api/render',{
    output_name: $('dlg-name').value||'output.mp4',
    output_dir:  $('dlg-dir').value,
  });
  if (d.error){ alert(d.error); btn.disabled=false; btn.textContent='Export'; return; }
  $('sb-msg').textContent = `${d.clips_count} clips → ${d.output}`;
  pollRender(btn);
}

async function pollRender(btn) {
  const d = await api('/api/render/log');
  const log = $('rp-log');
  log.innerHTML = d.log.map(l=>
    `<div class="${l.startsWith('[ERR')||l.startsWith('[EXC')?'err':'ok'}">${l}</div>`
  ).join('');
  log.scrollTop=log.scrollHeight;
  if (d.rendering){ setTimeout(()=>pollRender(btn),1500); return; }
  btn.disabled=false; btn.textContent='Export';
  closeDlg();
}

// ─── Keyboard ─────────────────────────────────────────────────────────────────
document.addEventListener('keydown', e=>{
  if (e.target.tagName==='INPUT') return;
  if ((e.key==='Delete'||e.key==='Backspace') && selAnchor>=0 && !e.ctrlKey && !e.metaKey){
    e.preventDefault(); cutSelection(); return;
  }
  if (e.key==='Escape'){ clearSelection(); return; }
  if ((e.ctrlKey||e.metaKey) && e.key==='z' && !e.shiftKey){ e.preventDefault(); doUndo(); return; }
  if ((e.ctrlKey||e.metaKey) && (e.key==='y' || (e.key==='z'&&e.shiftKey))){ e.preventDefault(); doRedo(); return; }
  if (e.key===' ' && selAnchor<0){ e.preventDefault(); togglePlay(); return; }
  if (e.key==='j') step(-5);
  if (e.key==='l') step(5);
  if (e.key==='k') player.pause();
  // Restore: Cmd+Delete or right-click menu (not implemented yet)
  // R key to restore selection
  if (e.key==='r' && selAnchor>=0){ restoreSelection(); }
});

// ─── Init ─────────────────────────────────────────────────────────────────────
async function init() {
  const st = await api('/api/state');
  if (st.video_path) {
    $('vpath').value = st.video_path;
    $('dlg-dir').value = st.output_dir || '';
    $('vol-in').value = st.volume;
    dur = st.duration;
    $('tc-tot').textContent = fmt(dur);
    player.src = '/video?t='+Date.now(); player.load();
    if (st.words_count>0) {
      const wd = await api('/api/words');
      words=wd.words; deleted=wd.deleted;
      renderTranscript(); updateStatus();
    }
    if (st.has_peaks) loadWaveform();
    else loadWaveform();
  }
  $('sb-vol').textContent = `Vol ${parseFloat(st.volume||3).toFixed(1)}x`;
}
init();
</script>
</body>
</html>
"""

@app.route("/")
def index(): return UI

# ─── Entry ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv)>1:
        p = sys.argv[1]
        if os.path.exists(p):
            try: d = get_dur(p)
            except: d = 0.0
            S.update({"video_path":p,"duration":d,
                      "output_dir":str(Path(p).parent)})
    print("http://localhost:3028")
    app.run(host="0.0.0.0", port=3028, debug=False, threaded=True)
