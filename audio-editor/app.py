"""
Audio Editor — transcript-driven manual audio editing.
The audio-only counterpart to video-editor.

Run: python app.py [audio_file]    ->    http://localhost:3029
"""
import os, sys, json, subprocess, tempfile, threading, struct
from pathlib import Path
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

S = {
    "audio_path": None,
    "duration":   0.0,
    "words":      [],
    "deleted":    [],
    "output_dir": None,
    "volume":     1.0,
    "peaks":      None,
    "transcribing": False,
    "transcribe_msg": "",
    "rendering":  False,
    "render_log": [],
}


def get_dur(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True, timeout=15)
    return float(json.loads(r.stdout)["format"]["duration"])


# ─── Streaming ──────────────────────────────────────────────────────────────
@app.route("/audio")
def audio():
    p = S["audio_path"]
    if not p or not os.path.exists(p):
        return "No audio loaded", 404
    size = os.path.getsize(p)
    rh = request.headers.get("Range", "")
    s, e = 0, size - 1
    if rh:
        pts = rh.replace("bytes=", "").split("-")
        s = int(pts[0]) if pts[0] else 0
        e = int(pts[1]) if len(pts) > 1 and pts[1].strip() else size - 1
    with open(p, "rb") as f:
        f.seek(s)
        data = f.read(e - s + 1)
    # Guess MIME
    ext = Path(p).suffix.lower()
    mime = {
        ".wav": "audio/wav", ".mp3": "audio/mpeg", ".m4a": "audio/mp4",
        ".flac": "audio/flac", ".ogg": "audio/ogg", ".opus": "audio/opus",
    }.get(ext, "audio/mpeg")
    return Response(data, status=206 if rh else 200, headers={
        "Content-Range": f"bytes {s}-{e}/{size}",
        "Accept-Ranges": "bytes", "Content-Length": str(e - s + 1),
        "Content-Type": mime})


# ─── API ────────────────────────────────────────────────────────────────────
@app.route("/api/state")
def state():
    return jsonify({
        "audio_path": S["audio_path"], "duration": S["duration"],
        "words_count": len(S["words"]),
        "deleted_count": sum(S["deleted"]) if S["deleted"] else 0,
        "volume": S["volume"],
        "transcribing": S["transcribing"], "transcribe_msg": S["transcribe_msg"],
        "rendering": S["rendering"], "output_dir": S["output_dir"],
        "has_peaks": S["peaks"] is not None,
    })


@app.route("/api/load", methods=["POST"])
def load():
    path = (request.json or {}).get("path", "").strip()
    if not path or not os.path.exists(path):
        return jsonify({"error": f"Not found: {path}"}), 400
    try: dur = get_dur(path)
    except: dur = 0.0
    S.update({"audio_path": path, "duration": dur, "words": [], "deleted": [],
              "output_dir": str(Path(path).parent), "peaks": None})
    return jsonify({"ok": True, "duration": dur})


@app.route("/api/waveform")
def waveform():
    if S["peaks"] is not None:
        return jsonify({"peaks": S["peaks"]})
    p = S["audio_path"]
    if not p: return jsonify({"peaks": []})
    try:
        sr = 8000
        r = subprocess.run(["ffmpeg", "-i", p, "-ac", "1", "-ar", str(sr),
                            "-f", "f32le", "-"], capture_output=True, timeout=120)
        n = len(r.stdout) // 4
        if not n: return jsonify({"peaks": []})
        samp = struct.unpack(f"{n}f", r.stdout)
        chunk = max(1, n // 3000)
        peaks = [round(max(abs(x) for x in samp[i:i+chunk]), 4) for i in range(0, n, chunk)]
        mx = max(peaks) if peaks else 1
        if mx > 0: peaks = [v/mx for v in peaks]
        S["peaks"] = peaks
        return jsonify({"peaks": peaks})
    except Exception as ex:
        return jsonify({"peaks": [], "error": str(ex)})


@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    if S["transcribing"]:
        return jsonify({"error": "Already running"}), 400
    p = S["audio_path"]
    if not p: return jsonify({"error": "No audio"}), 400
    model_size = (request.json or {}).get("model", "base")

    def run():
        S["transcribing"] = True; S["transcribe_msg"] = "Loading Whisper..."
        try:
            import whisper
            m = whisper.load_model(model_size)
            S["transcribe_msg"] = "Transcribing..."
            res = m.transcribe(p, word_timestamps=True)
            words = []
            for seg in res["segments"]:
                for w in seg.get("words", []):
                    words.append({"start": round(w["start"], 3),
                                  "end": round(w["end"], 3),
                                  "word": w["word"].strip()})
            S["words"] = words
            S["deleted"] = [False] * len(words)
            S["transcribe_msg"] = f"Done - {len(words)} words"
        except Exception as ex:
            S["transcribe_msg"] = f"Error: {ex}"
        finally:
            S["transcribing"] = False

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"ok": True})


@app.route("/api/words")
def words_api():
    return jsonify({"words": S["words"], "deleted": S["deleted"]})


@app.route("/api/set-deleted", methods=["POST"])
def set_deleted():
    d = request.json.get("deleted", [])
    if len(d) == len(S["words"]):
        S["deleted"] = [bool(x) for x in d]
    return jsonify({"ok": True})


@app.route("/api/volume", methods=["POST"])
def volume():
    S["volume"] = float((request.json or {}).get("volume", 1.0))
    return jsonify({"ok": True})


@app.route("/api/render", methods=["POST"])
def render():
    if S["rendering"]:
        return jsonify({"error": "Already rendering"}), 400
    data = request.json or {}
    words = S["words"]; deleted = S["deleted"]
    if not words: return jsonify({"error": "No transcript"}), 400

    clips = []
    in_clip = False; cs = ce = 0.0; PAD = 0.05
    for i, w in enumerate(words):
        if not deleted[i]:
            if not in_clip: cs = max(0, w["start"] - PAD); in_clip = True
            ce = w["end"] + PAD
        else:
            if in_clip: clips.append((round(cs, 3), round(ce, 3))); in_clip = False
    if in_clip: clips.append((round(cs, 3), round(min(ce, S["duration"]), 3)))
    if not clips: return jsonify({"error": "Everything is deleted"}), 400

    out_name = data.get("output_name", "edited.wav")
    out_dir = data.get("output_dir", S["output_dir"]) or S["output_dir"]
    out_path = str(Path(out_dir) / out_name)
    source = S["audio_path"]; vol = S["volume"]
    normalize = bool(data.get("normalize", False))

    def run():
        S["rendering"] = True; S["render_log"] = ["Starting render..."]
        tmpdir = tempfile.mkdtemp(prefix="ae_")
        try:
            # Determine output codec from extension
            ext = Path(out_name).suffix.lower()
            codec_map = {
                ".wav": ("pcm_s16le", []),
                ".mp3": ("libmp3lame", ["-q:a", "2"]),
                ".m4a": ("aac", ["-b:a", "256k"]),
                ".flac": ("flac", []),
                ".ogg": ("libvorbis", ["-q:a", "6"]),
            }
            codec, codec_args = codec_map.get(ext, ("pcm_s16le", []))

            clip_files = []
            for i, (cs, ce) in enumerate(clips):
                out = os.path.join(tmpdir, f"c{i:04d}.wav")
                r = subprocess.run([
                    "ffmpeg", "-y", "-i", source,
                    "-ss", str(cs), "-to", str(ce),
                    "-c:a", "pcm_s16le", "-ac", "2",
                    out
                ], capture_output=True, text=True, timeout=300)
                if r.returncode != 0:
                    S["render_log"].append(f"[ERR] clip {i+1}: {r.stderr[-200:]}"); return
                clip_files.append(out)
                S["render_log"].append(f"OK {i+1}/{len(clips)} ({ce-cs:.1f}s)")

            concat = os.path.join(tmpdir, "c.txt")
            with open(concat, "w") as f:
                for p in clip_files: f.write(f"file '{p}'\n")

            S["render_log"].append("Joining + processing audio...")

            # Build audio filter chain
            af_parts = []
            if normalize:
                af_parts.append("loudnorm=I=-16:TP=-1.5:LRA=11")
            if vol != 1.0:
                af_parts.append(f"volume={vol}")
            af = ",".join(af_parts) if af_parts else None

            cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat]
            if af: cmd += ["-af", af]
            cmd += ["-c:a", codec] + codec_args + [out_path]

            r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if r.returncode != 0:
                S["render_log"].append(f"[ERR] {r.stderr[-200:]}")
            else:
                S["render_log"].append(f"Done -> {out_path}")
        except Exception as ex:
            S["render_log"].append(f"[EXC] {ex}")
        finally:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
            S["rendering"] = False

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"ok": True, "clips_count": len(clips), "output": out_path})


@app.route("/api/render/log")
def render_log():
    return jsonify({"rendering": S["rendering"], "log": S["render_log"]})


# ─── UI ─────────────────────────────────────────────────────────────────────
UI = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Audio Editor</title>
<style>
*, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
:root {
  --bg:#111; --surf:#161616; --surf2:#1c1c1c;
  --border:#252525; --bd2:#2e2e2e;
  --txt:#d4d4d4; --txt2:#666; --txt3:#3a3a3a;
  --blue:#3b82f6; --green:#4ade80; --red:#dc2626;
}
html,body { height:100%; overflow:hidden; background:var(--bg); color:var(--txt);
  font:13px/1.5 "SF Pro Display","Segoe UI",system-ui,sans-serif; }
#shell { display:grid; grid-template-rows:46px 1fr 28px; height:100vh; }
#hdr { background:var(--surf); border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:6px; padding:0 14px; }
.brand { font-size:11px; font-weight:600; letter-spacing:2px; color:var(--txt2);
  text-transform:uppercase; margin-right:10px; }
.sep { width:1px; height:20px; background:var(--border); margin:0 3px; }
button { font:12px/1 "SF Pro Display","Segoe UI",system-ui,sans-serif;
  background:var(--surf2); border:1px solid var(--bd2); color:var(--txt);
  padding:5px 12px; border-radius:4px; cursor:pointer; transition:background .12s,border-color .12s; }
button:hover { background:#232323; border-color:#3a3a3a; }
button:disabled { opacity:.35; cursor:default; }
button.primary { background:#1e3a6a; border-color:var(--blue); color:#93c5fd; }
button.primary:hover { background:#254a80; }
button.ghost { background:transparent; border-color:transparent; color:var(--txt2); }
button.ghost:hover { background:var(--surf2); border-color:var(--bd2); color:var(--txt); }
input[type=text], input[type=number] { background:#0d0d0d; border:1px solid var(--bd2); color:var(--txt);
  padding:4px 8px; border-radius:3px; font:12px "JetBrains Mono","Consolas",monospace; }
input::placeholder { color:var(--txt3); }
#hdr-right { margin-left:auto; display:flex; align-items:center; gap:6px; }
#hdr-status { font-size:11px; color:var(--txt2); }
#main { display:grid; grid-template-rows:auto 1fr auto; overflow:hidden; }

#top-bar { display:flex; gap:6px; padding:8px 16px; border-bottom:1px solid var(--border); background:var(--surf); }
#top-bar input { flex:1; }

#tx-scroll { overflow-y:auto; padding:32px 48px; }
#tx { font-size:16px; line-height:2.2; color:var(--txt); outline:none; }
.w { display:inline; padding:1px 1px; border-radius:2px; cursor:text;
  transition:background .08s; white-space:pre-wrap; }
.w:hover { background:#1e1e1e; }
.w.del { color:var(--txt3); text-decoration:line-through; }
.w.sel { background:#1e3a5f; color:#93c5fd; }
.w.playing { background:#1a2e1a; color:var(--green); border-radius:2px; }
.take-sep { display:block; margin:12px 0 8px; border:none;
  border-top:1px solid var(--border); opacity:.5; }

#bottom { background:var(--surf); border-top:1px solid var(--border); padding:8px 12px;
  display:flex; flex-direction:column; gap:6px; }
#audio-row { display:flex; align-items:center; gap:8px; }
#audio-row audio { flex:0 0 320px; }
#audio-row .actions { display:flex; gap:6px; }
#wv-wrap { padding:0; }
canvas#wv { width:100%; height:48px; display:block; border-radius:3px; background:#0d0d0d; cursor:pointer; }
#timecode { font:12px "JetBrains Mono","Consolas",monospace; color:var(--txt2); }
#timecode span { color:var(--txt); }

#sb { background:#0d0d0d; border-top:1px solid var(--border);
  display:flex; align-items:center; gap:16px; padding:0 14px;
  font-size:11px; color:var(--txt2); overflow:hidden; }
#sb-stats { display:flex; gap:12px; }

#dlg { display:none; position:fixed; inset:0; background:rgba(0,0,0,.75); z-index:99;
  align-items:center; justify-content:center; }
#dlg .panel { background:#1c1c1c; border:1px solid #333; border-radius:8px; padding:24px; width:440px; }
#dlg h2 { font-size:14px; margin-bottom:16px; color:#d4d4d4; }
#dlg label { font-size:11px; color:#666; display:block; margin-bottom:4px; margin-top:10px; }
#dlg input[type=checkbox] { vertical-align:middle; margin-right:6px; }

#rp-log { font:11px "JetBrains Mono",monospace; color:var(--txt2); padding:6px 12px;
  background:#0d0d0d; border-top:1px solid var(--border); max-height:80px; overflow-y:auto; display:none; }
#rp-log.show { display:block; }
#rp-log .ok { color:#4ade80; } #rp-log .err { color:#f87171; }

::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--bd2); border-radius:3px; }
</style>
</head>
<body>
<div id="shell">

<header id="hdr">
  <div class="brand">Audio Editor</div>
  <button id="btn-tx" onclick="doTranscribe()">Transcribe</button>
  <div class="sep"></div>
  <button class="ghost" onclick="removeFillers()">Remove fillers</button>
  <button class="ghost" onclick="restoreAll()">Restore all</button>
  <div class="sep"></div>
  <button class="ghost" onclick="doUndo()" title="Ctrl+Z">↩ Undo</button>
  <button class="ghost" onclick="doRedo()" title="Ctrl+Shift+Z">↺ Redo</button>
  <div id="hdr-right">
    <span id="hdr-status"></span>
    <button class="primary" onclick="showRender()">Export ▸</button>
  </div>
</header>

<div id="main">
  <div id="top-bar">
    <input type="text" id="apath" placeholder="Audio file path…" onkeydown="if(event.key==='Enter')doLoad()">
    <button onclick="doLoad()">Open</button>
    <span id="sel-hint" style="font-size:11px;color:var(--txt2);align-self:center;margin-left:auto">Click to seek · Select then Delete to cut</span>
  </div>

  <div id="tx-scroll">
    <div id="tx">
      <span style="color:#333;font-size:14px">Load an audio file, then click Transcribe.<br><br>
      Select words and press <kbd style="background:#1e1e1e;padding:1px 6px;border-radius:3px;font-size:12px">Delete</kbd> to cut them.
      Deleted words show as <span style="text-decoration:line-through;color:#333">strikethrough</span>.
      Playback skips them automatically.</span>
    </div>
  </div>

  <div id="bottom">
    <div id="audio-row">
      <audio id="player" controls preload="metadata"></audio>
      <span id="timecode"><span id="tc-cur">00:00.000</span> / <span id="tc-tot">00:00.000</span></span>
    </div>
    <div id="wv-wrap"><canvas id="wv"></canvas></div>
  </div>

  <div id="rp-log"></div>
</div>

<div id="sb">
  <div id="sb-stats">
    <span id="sb-cuts">—</span>
    <span id="sb-kept">—</span>
    <span id="sb-vol">Vol 1.0×</span>
  </div>
</div>

</div>

<div id="dlg">
  <div class="panel">
    <h2>Export</h2>
    <label>Filename (extension determines format)</label>
    <input type="text" id="dlg-name" value="edited.wav" style="width:100%">
    <label>Destination folder</label>
    <input type="text" id="dlg-dir" style="width:100%" readonly>
    <label>Volume multiplier</label>
    <input type="number" id="dlg-vol" value="1.0" step="0.5" min="0.1" max="10" style="width:80px">
    <label><input type="checkbox" id="dlg-normalize"> Normalize (EBU R128 loudness, -16 LUFS)</label>
    <div style="display:flex;gap:8px;margin-top:16px">
      <button class="primary" onclick="doRender()">Export</button>
      <button onclick="closeDlg()">Cancel</button>
    </div>
  </div>
</div>

<script>
'use strict';
const player = document.getElementById('player');
let words = [], deleted = [], dur = 0, peaks = [];
let selAnchor = -1, selHead = -1, isSelecting = false;
let undoStack = [], redoStack = [];
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

async function doLoad() {
  const path = $('apath').value.trim(); if (!path) return;
  const d = await api('/api/load', {path});
  if (d.error) { alert(d.error); return; }
  dur = d.duration;
  $('tc-tot').textContent = fmt(dur);
  player.src = '/audio?t='+Date.now(); player.load();
  const st = await api('/api/state');
  $('dlg-dir').value = st.output_dir || '';
  words=[]; deleted=[]; renderTranscript(); loadWaveform();
}

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
  for (let px=0; px<W; px++) {
    const t = (px/W)*dur;
    let col = '#1a1a1a';
    if (words.length) {
      const wi = words.findIndex(w => t>=w.start && t<w.end);
      col = wi>=0 ? (deleted[wi] ? '#3a1a1a' : '#1e3a6a') : '#1a1a1a';
    }
    const pi = Math.floor(px/W*peaks.length);
    const amp = (peaks[pi]||0)*H*0.85;
    ctx.fillStyle=col;
    ctx.fillRect(px, (H-amp)/2, 1, Math.max(1,amp));
  }
  if (dur>0) {
    const px = Math.floor((player.currentTime/dur)*W);
    ctx.fillStyle='#ef4444'; ctx.fillRect(px,0,1,H);
  }
}
$('wv').addEventListener('click', e => {
  if (!dur) return;
  const r = $('wv').getBoundingClientRect();
  const t = ((e.clientX-r.left)/r.width)*dur;
  seekToKept(t);
});
function seekToKept(t) {
  for (let i=0;i<words.length;i++) {
    if (!deleted[i] && words[i].end > t) {
      player.currentTime = Math.max(t, words[i].start); return;
    }
  }
  if (!words.length) player.currentTime = t;
}

async function doTranscribe() {
  const btn = $('btn-tx'); btn.disabled=true; btn.textContent='Transcribing…';
  await api('/api/transcribe', {model:'base'}); pollTx(btn);
}
async function pollTx(btn) {
  const st = await api('/api/state');
  $('hdr-status').textContent = st.transcribe_msg;
  if (st.transcribing) { setTimeout(()=>pollTx(btn),1500); return; }
  const d = await api('/api/words'); words=d.words; deleted=d.deleted;
  undoStack=[]; redoStack=[];
  btn.disabled=false; btn.textContent='Transcribe';
  renderTranscript(); updateStatus();
}

function renderTranscript() {
  const tx = $('tx'); if (!words.length) return;
  tx.innerHTML='';
  words.forEach((w,i) => {
    if (i>0 && w.start-words[i-1].end > 2.5) {
      const hr = document.createElement('hr'); hr.className='take-sep'; tx.appendChild(hr);
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
  if (e.shiftKey && selAnchor>=0) { selHead=i; applySelectionVis(); e.preventDefault(); return; }
  selAnchor=i; selHead=i; isSelecting=true; applySelectionVis();
  if (!deleted[i]) player.currentTime = words[i].start;
  else for (let j=i;j<words.length;j++) { if (!deleted[j]){player.currentTime=words[j].start;break;} }
  e.preventDefault();
}
function wordMouseEnter(e) {
  if (!isSelecting) return; selHead = parseInt(this.dataset.i); applySelectionVis();
}
document.addEventListener('mouseup', () => { isSelecting=false; });
function applySelectionVis() {
  const lo=Math.min(selAnchor,selHead), hi=Math.max(selAnchor,selHead);
  document.querySelectorAll('.w').forEach((el,i) => el.classList.toggle('sel', i>=lo && i<=hi));
  updateSelHint(hi-lo+1);
}
function clearSelection() {
  selAnchor=-1; selHead=-1;
  document.querySelectorAll('.w.sel').forEach(el=>el.classList.remove('sel'));
  $('sel-hint').textContent='Click to seek · Select then Delete to cut';
}
function updateSelHint(n) {
  if (n<=0) { $('sel-hint').textContent='Click to seek · Select then Delete to cut'; return; }
  const secs = words.slice(Math.min(selAnchor,selHead), Math.max(selAnchor,selHead)+1)
    .reduce((a,w)=>a+w.end-w.start,0);
  $('sel-hint').textContent=`${n} word${n>1?'s':''} selected (${secs.toFixed(1)}s) — Delete to cut, R to restore`;
}
function applyDeleted() {
  document.querySelectorAll('.w').forEach((el,i) => el.classList.toggle('del', !!deleted[i]));
  drawWaveform(); updateStatus();
}

function cutSelection() {
  if (selAnchor<0) return;
  const lo=Math.min(selAnchor,selHead), hi=Math.max(selAnchor,selHead);
  pushUndo();
  for (let i=lo;i<=hi;i++) deleted[i]=true;
  clearSelection(); applyDeleted(); saveDeleted();
}
function restoreSelection() {
  if (selAnchor<0) return;
  const lo=Math.min(selAnchor,selHead), hi=Math.max(selAnchor,selHead);
  pushUndo();
  for (let i=lo;i<=hi;i++) deleted[i]=false;
  clearSelection(); applyDeleted(); saveDeleted();
}
function restoreAll() { pushUndo(); deleted=deleted.map(()=>false); applyDeleted(); saveDeleted(); }
function removeFillers() {
  if (!words.length) return;
  const F = new Set(["um","uh","hmm","uhh","umm","hm","ugh","mhm","mmm"]);
  pushUndo();
  words.forEach((w,i)=>{
    if (F.has(w.word.toLowerCase().replace(/[,.!?—\-]/g,''))) deleted[i]=true;
  });
  applyDeleted(); saveDeleted();
}

function pushUndo() { undoStack.push([...deleted]); redoStack=[]; if (undoStack.length>80) undoStack.shift(); }
function doUndo() { if (!undoStack.length) return; redoStack.push([...deleted]); deleted=undoStack.pop(); applyDeleted(); saveDeleted(); }
function doRedo() { if (!redoStack.length) return; undoStack.push([...deleted]); deleted=redoStack.pop(); applyDeleted(); saveDeleted(); }
async function saveDeleted() { await api('/api/set-deleted', {deleted}); }

let lastSkipAt = -1;
player.addEventListener('timeupdate', () => {
  const t = player.currentTime;
  $('tc-cur').textContent = fmt(t);
  drawWaveform();
  highlightWord(t);
  if (!words.length) return;
  const wi = words.findIndex(w => t>=w.start && t<w.end);
  if (wi>=0 && deleted[wi] && Math.abs(t-lastSkipAt)>0.3) {
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
player.addEventListener('loadedmetadata', () => { dur = player.duration; $('tc-tot').textContent = fmt(dur); });

function updateStatus() {
  const nDel = deleted.filter(Boolean).length;
  const kept = words.reduce((a,w,i)=>a+(deleted[i]?0:w.end-w.start),0);
  const total = words.reduce((a,w)=>a+w.end-w.start,0);
  $('sb-cuts').textContent = nDel>0 ? `${nDel} word${nDel>1?'s':''} cut` : 'No cuts';
  $('sb-kept').textContent = words.length ? `${kept.toFixed(1)}s of ${total.toFixed(1)}s kept` : '—';
}

function showRender() { $('dlg').style.display='flex'; }
function closeDlg()   { $('dlg').style.display='none'; }
$('dlg').addEventListener('click', e=>{ if(e.target===$('dlg')) closeDlg(); });

async function doRender() {
  const btn = $('dlg').querySelector('button.primary');
  btn.disabled=true; btn.textContent='Exporting…';
  $('rp-log').classList.add('show'); $('rp-log').innerHTML='';
  await api('/api/volume', {volume: parseFloat($('dlg-vol').value)||1.0});
  const d = await api('/api/render', {
    output_name: $('dlg-name').value||'edited.wav',
    output_dir:  $('dlg-dir').value,
    normalize:   $('dlg-normalize').checked,
  });
  if (d.error){ alert(d.error); btn.disabled=false; btn.textContent='Export'; return; }
  $('sb-stats').lastElementChild.textContent = `Vol ${parseFloat($('dlg-vol').value).toFixed(1)}x`;
  pollRender(btn);
}
async function pollRender(btn) {
  const d = await api('/api/render/log');
  $('rp-log').innerHTML = d.log.map(l =>
    `<div class="${l.startsWith('[ERR')||l.startsWith('[EXC')?'err':'ok'}">${l}</div>`).join('');
  $('rp-log').scrollTop = $('rp-log').scrollHeight;
  if (d.rendering) { setTimeout(()=>pollRender(btn),1500); return; }
  btn.disabled=false; btn.textContent='Export'; closeDlg();
}

document.addEventListener('keydown', e => {
  if (e.target.tagName==='INPUT') return;
  if ((e.key==='Delete'||e.key==='Backspace') && selAnchor>=0 && !e.ctrlKey && !e.metaKey){
    e.preventDefault(); cutSelection(); return;
  }
  if (e.key==='Escape'){ clearSelection(); return; }
  if ((e.ctrlKey||e.metaKey) && e.key==='z' && !e.shiftKey){ e.preventDefault(); doUndo(); return; }
  if ((e.ctrlKey||e.metaKey) && (e.key==='y' || (e.key==='z'&&e.shiftKey))){ e.preventDefault(); doRedo(); return; }
  if (e.key==='r' && selAnchor>=0){ restoreSelection(); }
  if (e.key===' ' && selAnchor<0){ e.preventDefault(); if (player.paused) player.play(); else player.pause(); }
});

async function init() {
  const st = await api('/api/state');
  if (st.audio_path) {
    $('apath').value = st.audio_path;
    $('dlg-dir').value = st.output_dir || '';
    dur = st.duration; $('tc-tot').textContent = fmt(dur);
    player.src = '/audio?t='+Date.now(); player.load();
    if (st.words_count>0) {
      const wd = await api('/api/words');
      words=wd.words; deleted=wd.deleted;
      renderTranscript(); updateStatus();
    }
    loadWaveform();
  }
}
init();
</script>
</body>
</html>
"""

@app.route("/")
def index(): return UI


if __name__ == "__main__":
    if len(sys.argv) > 1:
        p = sys.argv[1]
        if os.path.exists(p):
            try: d = get_dur(p)
            except: d = 0.0
            S.update({"audio_path": p, "duration": d,
                      "output_dir": str(Path(p).parent)})
    print("http://localhost:3029")
    app.run(host="0.0.0.0", port=3029, debug=False, threaded=True)
