import os

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_model = genai.GenerativeModel("models/gemini-1.5-pro")

_STORY_PROMPT = """You are a comic book writer. Expand the following panel-by-panel
outline into a full comic-style story with vivid narration and character dialogue.

Outline (JSON):
{outline}

For EACH panel, write:
- A short "caption" (ambient description of the environment/background)
- "narration" describing the character's actions, emotions, and/or dialogue

Format your response as plain text, clearly separated per panel, like:

Panel 1: <title>
Caption: ...
Narration: ...

Panel 2: <title>
Caption: ...
Narration: ...

...and so on for all panels.
"""


def generate_story(outline: list[dict]) -> str:
    """Use Gemini Pro to expand a panel outline into full narration + dialogue.

    Returns a single formatted text block covering every panel.
    """
    prompt = _STORY_PROMPT.format(outline=outline)
    response = _model.generate_content(prompt)
    return response.text.strip()
