# Video Editor

Descript-style transcript-driven cutting, free and local.

## Run

```bash
pip install flask openai-whisper
python app.py [optional_video_file.mp4]
```

Open `http://localhost:3028` in your browser.

## Workflow

1. Load video (paste path or pass as CLI arg)
2. Click **Transcribe**
3. Select words you want to cut → press **Delete**
4. Playback automatically skips cut words
5. Click **Export ▸** → render to file

## Keys

- `Space` — play/pause (when not selecting)
- `Delete` / `Backspace` — cut selected words
- `R` — restore selected (un-cut)
- `Ctrl+Z` / `Cmd+Z` — undo
- `Ctrl+Shift+Z` / `Ctrl+Y` — redo
- `J` / `L` — back / forward 5s
- `K` — pause
- `Esc` — clear selection

## Quick actions

- **Remove fillers** — strikes all um/uh/hmm/etc.
- **Remove false starts** — drops short takes (≤5 words) that aren't the final attempt
- **Restore all** — un-cut everything

See `SKILL.md` for full design context.
