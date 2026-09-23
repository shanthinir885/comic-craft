import os
import time

from fpdf import FPDF

_EXPORTS_DIR = os.path.join("static", "exports")


def save_pdf(layout: list[dict]) -> str:
    """Compile a comic layout into a multi-page PDF.

    Each panel's image and narration are placed on their own page.
    Returns the path to the saved PDF file.
    """
    os.makedirs(_EXPORTS_DIR, exist_ok=True)

    pdf = FPDF(unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 16)
        pdf.multi_cell(0, 10, f"Panel {panel['panel_number']}: {panel['title']}")
        pdf.ln(2)

        image_path = panel.get("image_path")
        if image_path and os.path.exists(image_path):
            pdf.image(image_path, w=170)
            pdf.ln(4)

        if panel.get("scene_description"):
            pdf.set_font("Helvetica", "I", 11)
            pdf.multi_cell(0, 7, panel["scene_description"])
            pdf.ln(2)

        if panel.get("caption"):
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, f"Caption: {panel['caption']}")
            pdf.ln(1)

        if panel.get("narration"):
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, f"Narration: {panel['narration']}")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"comiccraft_{timestamp}.pdf"
    filepath = os.path.join(_EXPORTS_DIR, filename)
    pdf.output(filepath)

    return filepath
