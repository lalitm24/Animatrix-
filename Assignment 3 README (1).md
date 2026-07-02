# Prompt-to-Animation Backend

Turns a plain-English prompt into a rendered Manim video, served over a small
FastAPI backend.

## Files

- `generate_scene.py` — the core engine: prompt → LLM → clean Manim code →
  rendered `.mp4`. Exposes `generate_animation_video(prompt: str) -> str`.
- `main.py` — FastAPI app that wraps the engine and exposes it over HTTP.
- `.env.example` — required environment variables (no real keys).

## Setup

1. **Install system dependency:** Manim needs FFmpeg and (for full LaTeX
   support) a LaTeX distribution. At minimum install FFmpeg:
   ```bash
   # macOS
   brew install ffmpeg
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   ```

2. **Create a virtual environment and install Python deps:**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install fastapi uvicorn python-dotenv anthropic manim
   ```

3. **Set up your API key:**
   ```bash
   cp .env.example .env
   # then edit .env and paste in your real ANTHROPIC_API_KEY
   ```
   `.env` is git-ignored — only `.env.example` should ever be committed.

## Running the server

```bash
python main.py
```

This starts the API at `http://localhost:8000` with hot-reload enabled
(fine for local dev; disable `reload=True` in `main.py` before deploying).

## Using the API

**Endpoint:** `POST /generate`

Request body:
```json
{
  "prompt": "A red circle that morphs into a blue square"
}
```

Response:
```json
{
  "video_url": "/media/videos/scene_ab12cd34/480p15/GeneratedScene.mp4"
}
```

Fetch the actual video from:
```
http://localhost:8000/media/videos/scene_ab12cd34/480p15/GeneratedScene.mp4
```

## Testing without the API

You can test the core engine directly:
```bash
python generate_scene.py "a triangle that spins and shrinks"
```

## Notes

- Rendering uses `-ql` (low quality) for fast turnaround during development.
  Switch to `-qh` in `generate_scene.py` for higher quality output.
- If the LLM returns code that fails to compile/render, the API responds with
  a `422` (bad/invalid generated code) or `500` (render failure) and a
  descriptive error message instead of crashing.
