"""
generate_scene.py
------------------
Core "prompt -> animation" engine.

Flow:
    prompt (str)
        -> send to LLM with strict prompt-engineering
        -> extract clean Manim python code from the response
        -> save code to a .py file
        -> run `manim` on it via subprocess
        -> return path to the rendered .mp4

Only generate_animation_video() should be imported/used by main.py.
"""

import os
import re
import uuid
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic

# --------------------------------------------------------------------------- #
# Week 1 Checkpoint — load credentials, set up the client
# --------------------------------------------------------------------------- #

load_dotenv()  # reads .env in the current working directory

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

if not API_KEY:
    raise RuntimeError(
        "ANTHROPIC_API_KEY not found. Create a .env file (see .env.example) "
        "and set your API key there."
    )

client = Anthropic(api_key=API_KEY)

# Where generated code + rendered videos live
BASE_DIR = Path(__file__).resolve().parent
SCENES_DIR = BASE_DIR / "generated_scenes"
MEDIA_DIR = BASE_DIR / "media"
SCENES_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)

SCENE_CLASS_NAME = "GeneratedScene"


# --------------------------------------------------------------------------- #
# Week 2 Checkpoint — prompt engineering so the LLM ONLY returns Manim code
# --------------------------------------------------------------------------- #

SYSTEM_PROMPT = f"""You are a Manim (Community Edition) code generator.

Rules you MUST follow, no exceptions:
1. Output ONLY valid, runnable Python code for Manim Community Edition.
2. The code must define exactly one Scene subclass named `{SCENE_CLASS_NAME}`.
3. Do NOT include markdown code fences (no ```python or ```).
4. Do NOT include any explanation, commentary, or text before/after the code.
5. Import everything you need at the top (e.g. `from manim import *`).
6. Keep the animation short (under 15 seconds) and make sure every object used
   is defined before it is animated.
7. Do not use any external assets (no images, sounds, or files) — only Manim's
   built-in shapes, text, and mobjects.

Your entire response must be nothing but the Python source code.
"""


def _call_llm(prompt: str) -> str:
    """Send the user's prompt to the LLM and return the raw text response."""
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Create a Manim scene for the following request:\n\n"
                    f"{prompt}\n\n"
                    f"Remember: class must be named {SCENE_CLASS_NAME}, "
                    f"output raw code only."
                ),
            }
        ],
    )
    # response.content is a list of blocks; we only sent a text-only prompt
    # so we expect a single text block back.
    return "".join(block.text for block in response.content if block.type == "text")


# --------------------------------------------------------------------------- #
# Week 3 Checkpoint — extract clean python code from the raw LLM response
# --------------------------------------------------------------------------- #

def _extract_code(raw_response: str) -> str:
    """
    Strip markdown fences / stray commentary and return just the python code.
    Handles cases where the model ignores instructions and wraps code in
    ```python ... ``` fences anyway.
    """
    text = raw_response.strip()

    # Prefer a fenced code block if one exists.
    fence_match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    if fence_match:
        code = fence_match.group(1).strip()
    else:
        code = text

    if "class " not in code or "Scene" not in code:
        raise ValueError("LLM response did not contain a valid Manim Scene class.")

    return code


# --------------------------------------------------------------------------- #
# Week 4 Checkpoint — save code to disk + render with manim via subprocess
# --------------------------------------------------------------------------- #

def _save_code(code: str) -> Path:
    file_id = uuid.uuid4().hex[:8]
    file_path = SCENES_DIR / f"scene_{file_id}.py"
    file_path.write_text(code, encoding="utf-8")
    return file_path


def _render_scene(file_path: Path) -> Path:
    """
    Run manim on the generated file. Returns the path to the rendered mp4.
    Raises RuntimeError with manim's stderr if rendering fails.
    """
    cmd = [
        "manim",
        "-ql",                       # low quality -> fast render for dev/demo
        "--media_dir", str(MEDIA_DIR),
        str(file_path),
        SCENE_CLASS_NAME,
    ]

    result = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
        timeout=180,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Manim failed to render the scene.\n--- stderr ---\n{result.stderr}"
        )

    # manim -ql output path pattern:
    # media/videos/<scene_file_stem>/480p15/<SceneClassName>.mp4
    expected_dir = MEDIA_DIR / "videos" / file_path.stem / "480p15"
    video_path = expected_dir / f"{SCENE_CLASS_NAME}.mp4"

    if not video_path.exists():
        # Fall back to searching for any mp4 manim produced for this scene
        matches = list(MEDIA_DIR.rglob(f"{SCENE_CLASS_NAME}.mp4"))
        if not matches:
            raise RuntimeError("Manim reported success but no .mp4 file was found.")
        video_path = matches[0]

    return video_path


# --------------------------------------------------------------------------- #
# Week 5 Checkpoint — glue everything together, handle failures gracefully
# --------------------------------------------------------------------------- #

def generate_animation_video(prompt: str) -> str:
    """
    Turn a plain-English prompt into a rendered Manim video.

    Returns:
        str: absolute path to the rendered .mp4 file.

    Raises:
        ValueError: if the prompt is empty or the LLM's code is unusable.
        RuntimeError: if rendering fails for any reason.
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must not be empty.")

    try:
        raw_response = _call_llm(prompt)
    except Exception as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    try:
        code = _extract_code(raw_response)
    except ValueError as exc:
        raise ValueError(f"Could not extract valid Manim code: {exc}") from exc

    file_path = _save_code(code)

    try:
        video_path = _render_scene(file_path)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Rendering timed out.") from exc
    except RuntimeError:
        raise  # already has a useful message

    return str(video_path.resolve())


if __name__ == "__main__":
    # Quick manual test: python generate_scene.py "a blue circle turning into a square"
    import sys

    test_prompt = " ".join(sys.argv[1:]) or "A red circle that morphs into a blue square"
    print(f"Generating animation for prompt: {test_prompt!r}")
    path = generate_animation_video(test_prompt)
    print(f"Done! Video saved at: {path}")
