# Wardrobe Pick 👗✦

AI-powered capsule wardrobe planner for travel — plus a personal wardrobe manager.

## Features

- **Trip Planner** — enter destination, days, and season to get a curated capsule wardrobe with outfit suggestions and packing tips
- **My Wardrobe** — add your own outfits with photos, category, season, color, and notes; filter by category; delete when needed

## Quick Start

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
uvicorn main:app --reload

# 4. Open in browser
# http://127.0.0.1:8000
```

## Project Structure

```
wardrobe_pick/
├── main.py                  # FastAPI app entry point
├── requirements.txt
├── data/
│   └── my_wardrobe.json     # auto-created — stores user outfits
├── routers/
│   ├── outfit.py            # Trip planner routes (/, /generate)
│   └── wardrobe.py          # My Wardrobe routes (/my-wardrobe/...)
├── services/
│   ├── outfit_generator.py  # Rule-based capsule wardrobe logic
│   └── wardrobe_data.py     # Built-in clothing catalogue
├── templates/
│   ├── index.html           # Home / Trip planner
│   ├── results.html         # Generated outfit results
│   └── my_wardrobe.html     # Personal wardrobe manager
└── static/
    ├── css/style.css
    ├── js/app.js
    ├── js/wardrobe.js
    └── images/
        ├── placeholder.svg
        └── uploads/         # auto-created — user-uploaded photos
```

## Notes

- Outfit data and uploaded images persist across restarts (stored in `data/` and `static/images/uploads/`)
- Max upload size: 5 MB per image (JPG, PNG, WEBP, GIF)
- The trip planner is rule-based; swap `services/outfit_generator.py` with an LLM call for AI recommendations
