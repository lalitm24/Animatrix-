"""
backend.py

FastAPI server for generating Manim animations from text prompts.

Run:
    python backend.py

or

    uvicorn backend:app --reload --port 8000
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from generate_scene import generate_animation_video, MEDIA_DIR


# -------------------------------------------------------------
# FastAPI Application
# -------------------------------------------------------------

app = FastAPI(
    title="Animation Generation Service"
)


# -------------------------------------------------------------
# Request Model
# -------------------------------------------------------------

class PromptPayload(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        description="Animation description in plain English."
    )


# -------------------------------------------------------------
# Middleware
# -------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# Static Files
# -------------------------------------------------------------

MEDIA_DIR.mkdir(exist_ok=True, parents=True)

app.mount(
    "/media",
    StaticFiles(directory=str(MEDIA_DIR)),
    name="generated_media",
)


# -------------------------------------------------------------
# Helper Function
# -------------------------------------------------------------

def create_video(prompt_text: str) -> str:
    """
    Calls the animation generation pipeline and
    returns the relative URL of the rendered video.
    """

    output_file = generate_animation_video(prompt_text)

    relative_file = Path(output_file).relative_to(MEDIA_DIR)

    return f"/media/{relative_file.as_posix()}"


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------

@app.get("/")
def health():
    return {
        "status": "ok",
        "message": "Backend is active."
    }


@app.post("/generate")
def generate_video(data: PromptPayload):

    try:
        generated_url = create_video(data.prompt)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {error}"
        )

    return {
        "video_url": generated_url
    }


# -------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
