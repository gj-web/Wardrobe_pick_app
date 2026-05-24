"""
Wardrobe Router
===============
Handles user's personal wardrobe: add, view, and delete outfits.
Images are stored in static/images/uploads/.
Outfit data is persisted to data/my_wardrobe.json.
"""

import json
import os
import shutil
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/my-wardrobe", tags=["wardrobe"])
templates = Jinja2Templates(directory="templates")

DATA_FILE = Path("data/my_wardrobe.json")
UPLOAD_DIR = Path("static/images/uploads")

# Ensure directories exist
DATA_FILE.parent.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE_MB = 5


def _load_wardrobe() -> list:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save_wardrobe(items: list) -> None:
    DATA_FILE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


@router.get("/", response_class=HTMLResponse)
async def my_wardrobe(request: Request):
    """Show the user's personal wardrobe page."""
    items = _load_wardrobe()
    return templates.TemplateResponse(
        "my_wardrobe.html",
        {"request": request, "outfits": items, "total": len(items)},
    )


@router.post("/add")
async def add_outfit(
    request: Request,
    name: str = Form(...),
    category: str = Form(...),
    season: str = Form(...),
    color: str = Form(...),
    notes: str = Form(""),
    image: Optional[UploadFile] = File(None),
):
    """Add a new outfit item to the user's wardrobe."""
    items = _load_wardrobe()

    # Handle image upload
    image_url = "/static/images/placeholder.svg"
    if image and image.filename:
        ext = Path(image.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Use: {', '.join(ALLOWED_EXTENSIONS)}",
            )

        # Read and check size
        contents = await image.read()
        if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max {MAX_FILE_SIZE_MB}MB.",
            )

        filename = f"{uuid.uuid4().hex}{ext}"
        dest = UPLOAD_DIR / filename
        dest.write_bytes(contents)
        image_url = f"/static/images/uploads/{filename}"

    new_item = {
        "id": uuid.uuid4().hex,
        "name": name.strip(),
        "category": category,
        "season": season,
        "color": color.strip(),
        "notes": notes.strip(),
        "image": image_url,
    }

    items.append(new_item)
    _save_wardrobe(items)

    return RedirectResponse(url="/my-wardrobe", status_code=303)


@router.post("/delete/{item_id}")
async def delete_outfit(item_id: str):
    """Delete an outfit item by ID."""
    items = _load_wardrobe()
    item_to_delete = next((i for i in items if i["id"] == item_id), None)

    if item_to_delete:
        # Remove uploaded image file if it's a local upload
        img_path = item_to_delete.get("image", "")
        if img_path.startswith("/static/images/uploads/"):
            local_path = Path(img_path.lstrip("/"))
            if local_path.exists():
                local_path.unlink()

        items = [i for i in items if i["id"] != item_id]
        _save_wardrobe(items)

    return RedirectResponse(url="/my-wardrobe", status_code=303)
