from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app.exporters import save_pdf
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.models import PromptRequest

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _run_pipeline(story_prompt: str, character_name: str, setting: str,
                   tone: str, art_style: str):
    """Shared generation pipeline used by both /generate and /generate-comic/json."""
    outline = generate_outline(story_prompt, character_name, setting, tone, art_style)
    story_text = generate_story(outline)

    images = {}
    for panel in outline:
        num = panel.get("panel_number")
        images[num] = generate_image(panel.get("image_prompt", ""))

    layout = build_comic_layout(outline, story_text, images)
    pdf_path = save_pdf(layout)

    return layout, pdf_path


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate")
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        layout, pdf_path = _run_pipeline(
            story_prompt, character_name, setting, tone, art_style
        )
    except Exception as exc:  # noqa: BLE001 - surface as a clean 500
        raise HTTPException(status_code=500, detail=f"Comic generation failed: {exc}")

    return templates.TemplateResponse(
        "comic_preview.html",
        {"request": request, "layout": layout, "pdf_path": pdf_path},
    )


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        layout, pdf_path = _run_pipeline(
            payload.story_prompt,
            payload.character_name,
            payload.setting,
            payload.tone,
            payload.art_style,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Comic generation failed: {exc}")

    return JSONResponse({"layout": layout, "pdf_path": pdf_path})


@router.get("/export-success")
async def export_success(request: Request, pdf_path: str = ""):
    return templates.TemplateResponse(
        "export_success.html", {"request": request, "pdf_path": pdf_path}
    )


@router.post("/test-image")
async def test_image(prompt: str = Form(...)):
    try:
        image_path = generate_image(prompt)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Image generation failed: {exc}")

    return JSONResponse({"image_path": image_path})
