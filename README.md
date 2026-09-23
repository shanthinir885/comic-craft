# ComicCraft — AI Comic Story Creator

Turns a story prompt into a full AI-generated comic: structured panel outline
(Gemini Flash) → narration & dialogue (Gemini Pro) → illustrations (Stable
Diffusion) → viewable preview → downloadable PDF.

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv comiccraft-env
   # Windows
   comiccraft-env\Scripts\activate
   # macOS/Linux
   source comiccraft-env/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   HF_API_KEY=your_huggingface_api_key_here
   ```

4. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

5. Open the app:
   - App: http://127.0.0.1:8000
   - API docs: http://127.0.0.1:8000/docs

## Routes

| Route                     | Method | Purpose                                         |
|---------------------------|--------|--------------------------------------------------|
| `/`                       | GET    | Homepage — input form                            |
| `/generate`               | POST   | Form-based comic generation → preview page       |
| `/generate-comic/json`    | POST   | JSON API version, returns layout + PDF path       |
| `/export-success`         | GET    | Export confirmation page                          |
| `/test-image`             | POST   | Test image generation for a single prompt          |

## Project Structure

```
app/
  main.py            FastAPI app entrypoint
  routes.py          All route definitions
  models.py           Pydantic schemas
  gemini_flash.py      Panel outline generation
  gemini_pro.py        Narration & dialogue generation
  image_generator.py   Stable Diffusion illustration generation
  layout_builder.py    Combines outline + story + images into one layout
  exporters.py         PDF export via FPDF
templates/            Jinja2 HTML templates
static/panels/        Generated panel images
static/exports/       Generated PDFs
```

## Notes

- Every comic is generated fresh — no caching, no user accounts in this version.
- Add a `static/images/background.jpg` for the homepage's scenic background
  (any landscape image works, or remove that CSS rule).
- First image generation will download the Stable Diffusion weights (~4GB) —
  this can take a while and needs a GPU for reasonable speed (CPU works but is slow).
