from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.outfit_generator import generate_outfits

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page with trip planning form and My Wardrobe section."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    destination: str = Form(...),
    days: int = Form(...),
    season: str = Form(...),
):
    """Process the form and return a capsule wardrobe plan."""
    days = max(1, min(days, 30))
    destination = destination.strip() or "Your Destination"

    plan = generate_outfits(destination=destination, days=days, season=season)

    return templates.TemplateResponse(
        "results.html",
        {"request": request, "plan": plan},
    )
