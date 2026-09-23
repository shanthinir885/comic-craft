import re


def _parse_story(story_text: str) -> dict[int, dict]:
    """Parse Gemini Pro's formatted story text into a dict keyed by panel number.

    Expects blocks like:
        Panel 1: Title
        Caption: ...
        Narration: ...
    """
    panels = {}
    blocks = re.split(r"\n(?=Panel\s+\d+\s*:)", story_text.strip())

    for block in blocks:
        header_match = re.match(r"Panel\s+(\d+)\s*:\s*(.*)", block.strip())
        if not header_match:
            continue
        panel_number = int(header_match.group(1))
        title = header_match.group(2).strip()

        caption_match = re.search(r"Caption:\s*(.*?)(?:\nNarration:|$)", block, re.S)
        narration_match = re.search(r"Narration:\s*(.*)", block, re.S)

        panels[panel_number] = {
            "title": title,
            "caption": caption_match.group(1).strip() if caption_match else "",
            "narration": narration_match.group(1).strip() if narration_match else "",
        }

    return panels


def build_comic_layout(outline: list[dict], story_text: str,
                        images: dict[int, str]) -> list[dict]:
    """Combine outline, narration/dialogue, and generated images into one layout.

    Args:
        outline: list of panel dicts from generate_outline()
        story_text: raw text from generate_story()
        images: dict mapping panel_number -> image file path

    Returns:
        list of dicts, one per panel, sorted by panel_number:
        {panel_number, title, scene_description, image_path,
         caption, narration, image_prompt}
    """
    parsed_story = _parse_story(story_text)
    layout = []

    for panel in outline:
        num = panel.get("panel_number")
        story_bits = parsed_story.get(num, {})

        layout.append({
            "panel_number": num,
            "title": panel.get("title") or story_bits.get("title", ""),
            "scene_description": panel.get("scene_description", ""),
            "image_prompt": panel.get("image_prompt", ""),
            "image_path": images.get(num, ""),
            "caption": story_bits.get("caption", ""),
            "narration": story_bits.get("narration", ""),
        })

    layout.sort(key=lambda p: p["panel_number"] or 0)
    return layout
