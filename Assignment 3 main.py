"""
main.py
-------
FastAPI backend that wraps generate_scene.py.

Run locally with:
    python main.py
or
    uvicorn main:app --reload --port 8000
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from generate_scene import generate_animation_video, MEDIA_DIR

# --------------------------------------------------------------------------- #
# Checkpoint 1 — App setup
# --------------------------------------------------------------------------- #

app = FastAPI(title="Prompt-to-Animation API")


@app.get("/")
def root():
    return {"status": "ok", "message": "Prompt-to-Animation API is running."}


# --------------------------------------------------------------------------- #
# Checkpoint 2 — Request shape
# --------------------------------------------------------------------------- #

class GenerateRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        description="Plain-English description of the animation to generate.",
    )


# --------------------------------------------------------------------------- #
# Checkpoint 4 — CORS + static video hosting
# --------------------------------------------------------------------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten this to your frontend's origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")


# --------------------------------------------------------------------------- #
# Checkpoint 3 & 5 — Real logic + error handling
# --------------------------------------------------------------------------- #

@app.post("/generate")
def generate(request: GenerateRequest):
    try:
        video_path = generate_animation_video(request.prompt)
    except ValueError as exc:
        # Bad prompt or bad/unusable LLM code
        raise HTTPException(status_code=422, detail=str(exc))
    except RuntimeError as exc:
        # LLM call failed or manim rendering failed
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:  # noqa: BLE001 - final safety net
        raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}")

    # Build a URL relative to the mounted /media static route
    rel_path = Path(video_path).relative_to(MEDIA_DIR)
    video_url = f"/media/{rel_path.as_posix()}"

    return {"video_url": video_url}


# --------------------------------------------------------------------------- #
# Checkpoint 6 — Run the server
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import uvicorn

    # Port 8000 is FastAPI's usual default; match whatever your frontend
    # points at (e.g. http://localhost:8000).
    #
    # reload=True re-imports your app on every file save, which is great for
    # local development but should NEVER be used in production: it spawns a
    # file-watcher process, adds overhead, and can drop in-flight requests
    # when it restarts the server mid-render. We enable it here only because
    # this is a dev/demo backend.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
