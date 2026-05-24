# Wardrobe Pick 👗✦

AI-powered capsule wardrobe planner for travel — plus a personal wardrobe manager.

## Project Description

Wardrobe Pick is a web application created as a team project by Lina Dimova and Eva Gjorgjova.

The application consists of two main modules:

- **Trip Planner** – generates outfit combinations based on destination, season, and trip duration
- **My Wardrobe** – allows users to manage a personal clothing collection with images, categories, and notes

The main goal of the project is to simplify travel outfit planning by generating practical capsule wardrobe recommendations and helping users organize their personal outfits.

The project combines backend logic, frontend design, and basic project management practices. Jira was used for task organization, while GitHub was used for version control and source code management.

## Features

- **Trip Planner**
  - Enter destination, number of days, and season
  - Generates capsule wardrobe outfit plan
  - Provides packing tips and outfit combinations

- **My Wardrobe**
  - Add personal outfits with images
  - Store category, season, color, and notes
  - Filter outfits by category
  - Delete saved outfits

## Technologies Used

- Python
- FastAPI
- HTML
- CSS
- JavaScript
- Jinja2 Templates
- GitHub
- Jira

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
uvicorn main:app --reload

# 4. Open in browser
http://127.0.0.1:8000
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

## Team
Lina Dimova
Eva Gjorgjova