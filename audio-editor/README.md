# Audio Editor

Transcript-driven manual audio editing. The audio-only counterpart to [video-editor](../video-editor/).

## When to use

- Podcasts, voiceover passes, audio essays
- Any spoken-word audio where you'd rather edit by reading than by scrubbing
- Audio prep before dropping into a video editor

For video-with-audio, use video-editor (it has the video preview that helps spot bad takes).

## Run

```bash
pip install flask openai-whisper
python app.py [audio_file]
```

Opens at `http://localhost:3029` (different port from video-editor so you can run both).

Supports `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.opus` — anything ffmpeg decodes.

## Workflow

1. Load → Transcribe → Read along
2. Select stumbles → press `Delete`
3. Quick-clean with "Remove fillers" (um/uh/hmm)
4. Click `Export ▸` → choose format + volume + optional EBU R128 normalization

## Keys

Same as video-editor:
- `Space` play/pause · `J`/`L` skip 5s · `K` pause
- `Delete`/`Backspace` cut selection
- `R` restore selection
- `Ctrl+Z` / `Ctrl+Shift+Z` undo/redo
- `Esc` clear selection

See `SKILL.md` for the design.
