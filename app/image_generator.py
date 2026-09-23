import os
import re
import time

import torch
from diffusers import StableDiffusionPipeline

_MODEL_ID = "runwayml/stable-diffusion-v1-5"
_PANELS_DIR = os.path.join("static", "panels")

_device = "cuda" if torch.cuda.is_available() else "cpu"
_dtype = torch.float16 if _device == "cuda" else torch.float32

_pipeline = None


def _get_pipeline() -> StableDiffusionPipeline:
    """Lazily load the Stable Diffusion pipeline (expensive, so load once)."""
    global _pipeline
    if _pipeline is None:
        _pipeline = StableDiffusionPipeline.from_pretrained(
            _MODEL_ID, torch_dtype=_dtype
        )
        _pipeline = _pipeline.to(_device)
    return _pipeline


def _sanitize_filename(prompt: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", prompt.strip().lower())[:60].strip("_")
    return f"{slug}_{int(time.time())}.png"


def generate_image(image_prompt: str) -> str:
    """Generate a comic-style illustration for the given prompt.

    Saves the image under static/panels/ and returns the file path.
    """
    os.makedirs(_PANELS_DIR, exist_ok=True)
    pipeline = _get_pipeline()

    result = pipeline(image_prompt, num_inference_steps=30)
    image = result.images[0]

    filename = _sanitize_filename(image_prompt)
    filepath = os.path.join(_PANELS_DIR, filename)
    image.save(filepath)

    return filepath
