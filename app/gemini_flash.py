import json
import os
import re

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_model = genai.GenerativeModel("models/gemini-1.5-flash")

_OUTLINE_PROMPT = """You are a comic book outline generator.

Create a structured 5-panel comic outline for a story with these details:
- Story idea: {story_prompt}
- Main character: {character_name}
- Setting: {setting}
- Tone: {tone}
- Art style: {art_style}

Return ONLY valid JSON: a list of exactly 5 objects, each with keys:
"panel_number" (int), "title" (string), "scene_description" (string),
"image_prompt" (string — a detailed visual description suitable for an
image-generation model, incorporating the art style).
No markdown fences, no commentary — JSON only.
"""


def generate_outline(story_prompt: str, character_name: str, setting: str,
                      tone: str, art_style: str) -> list[dict]:
    """Use Gemini Flash to produce a structured 5-panel comic outline.

    Returns a list of dicts, one per panel:
    {panel_number, title, scene_description, image_prompt}
    """
    prompt = _OUTLINE_PROMPT.format(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style,
    )

    response = _model.generate_content(prompt)
    text = response.text.strip()

    # Strip markdown fences if the model added them anyway
    text = re.sub(r"^```(json)?|```$", "", text, flags=re.MULTILINE).strip()

    try:
        outline = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Gemini Flash returned invalid JSON: {exc}\nRaw: {text}")

    if not isinstance(outline, list):
        raise ValueError("Expected a JSON list of panel objects from Gemini Flash")

    return outline
