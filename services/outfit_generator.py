"""
Outfit Generator Service
========================
Rule-based capsule wardrobe planner for travel.
Designed to be swapped for AI/ML recommendations in a future upgrade.
"""

import random
from typing import List, Dict, Any, Optional
from services.wardrobe_data import WARDROBE


# ── Climate mapping ────────────────────────────────────────────────────────────

def season_to_climate(season: str) -> str:
    """Map user-provided season/temperature label to internal climate tag."""
    season = season.lower().strip()
    mapping = {
        "summer": "hot",
        "hot":    "hot",
        "spring": "warm",
        "warm":   "warm",
        "autumn": "mild",
        "fall":   "mild",
        "mild":   "mild",
        "cool":   "mild",
        "winter": "cold",
        "cold":   "cold",
        "freezing": "cold",
    }
    return mapping.get(season, "mild")


# ── Helper: filter wardrobe ────────────────────────────────────────────────────

def _get_items(category: str, style: str, climate: str, exclude_ids: Optional[set] = None) -> List[Dict]:
    """Return wardrobe items matching category, style tag, and climate tag."""
    exclude_ids = exclude_ids or set()
    return [
        item for item in WARDROBE
        if item["category"] == category
        and style in item["style"]
        and climate in item["climate"]
        and item["id"] not in exclude_ids
    ]


def _pick(category: str, style: str, climate: str, used: set) -> Optional[Dict]:
    """Pick one item, preferring unused items to maximise variety."""
    candidates = _get_items(category, style, climate, used)
    if not candidates:
        # Relax "used" constraint as fallback
        candidates = _get_items(category, style, climate)
    if not candidates:
        return None
    item = random.choice(candidates)
    used.add(item["id"])
    return item


# ── Outfit builders ────────────────────────────────────────────────────────────

def _build_outfit(style: str, climate: str, used: set, label: str) -> Dict[str, Any]:
    """
    Build a single outfit dict.  Rules:
    - dress outfits  → dress + shoes (heels/sandals for evening, else flats)
    - other outfits  → top + bottom + shoes
    - cold climate   → always add jacket / layering piece
    - evening style  → prefer fancier shoes
    """
    items = []

    use_dress = (style == "evening" and climate in ("warm", "mild", "cold")) or \
                (style == "casual" and climate in ("hot", "warm") and random.random() < 0.4)

    if use_dress:
        dress = _pick("dresses", style, climate, used)
        if dress is None:
            dress = _pick("dresses", "casual", climate, used)
        if dress:
            items.append(dress)

        # Shoes: heels for evening, sandals for warm casual, boots for cold
        if style == "evening":
            shoes = _pick("shoes", "evening", climate, used)
        elif climate in ("hot", "warm"):
            shoes = _pick("shoes", "casual", climate, used)
        else:
            shoes = _pick("shoes", style, climate, used)
        if shoes:
            items.append(shoes)
    else:
        # Top
        top = _pick("tops", style, climate, used)
        if top is None:
            top = _pick("tops", "casual", climate, used)
        if top:
            items.append(top)

        # Bottom
        bottom = _pick("bottoms", style, climate, used)
        if bottom is None:
            bottom = _pick("bottoms", "casual", climate, used)
        if bottom:
            items.append(bottom)

        # Shoes
        shoes = _pick("shoes", style, climate, used)
        if shoes is None:
            shoes = _pick("shoes", "casual", climate, used)
        if shoes:
            items.append(shoes)

    # Cold / mild → add outer layer
    if climate in ("cold", "mild"):
        jacket = _pick("jackets", style, climate, used)
        if jacket is None:
            jacket = _pick("jackets", "casual", climate, used)
        if jacket:
            items.append(jacket)

    return {
        "label": label,
        "style": style,
        "items": items,
    }


# ── Main generator ─────────────────────────────────────────────────────────────

def generate_outfits(destination: str, days: int, season: str) -> Dict[str, Any]:
    """
    Generate a capsule wardrobe plan.

    Outfit allocation (per trip length):
      1–2 days  → 1 casual, 1 evening
      3–4 days  → 2 casual, 1 evening, 1 backup
      5–7 days  → 3 casual, 1 evening, 1 smart-casual, 1 backup
      8+ days   → 4 casual, 2 evening, 1 smart-casual, 2 backup
    """
    climate = season_to_climate(season)
    random.seed(destination.lower() + str(days) + season.lower())  # reproducible per query
    used_ids: set = set()
    outfits = []

    # Determine outfit counts
    if days <= 2:
        plan = [("casual", 1), ("evening", 1)]
    elif days <= 4:
        plan = [("casual", 2), ("evening", 1), ("casual", 1)]  # last casual = backup
    elif days <= 7:
        plan = [("casual", 3), ("evening", 1), ("smart-casual", 1), ("casual", 1)]
    else:
        plan = [("casual", 4), ("evening", 2), ("smart-casual", 1), ("casual", 2)]

    label_counters: Dict[str, int] = {}

    for i, (style, count) in enumerate(plan):
        for _ in range(count):
            is_backup = (i == len(plan) - 1 and style == "casual" and days > 2)
            label_counters.setdefault(style, 0)
            label_counters[style] += 1

            if is_backup:
                label = f"Backup Outfit"
            elif style == "casual":
                label = f"Casual Outfit {label_counters[style]}"
            elif style == "evening":
                n = label_counters[style]
                label = "Evening Look" if n == 1 else f"Evening Look {n}"
            else:
                label = "Smart-Casual Look"

            outfit = _build_outfit(style, climate, used_ids, label)
            outfits.append(outfit)

    # Packing tips based on climate
    tips = _get_packing_tips(climate, days)

    return {
        "destination": destination.title(),
        "days": days,
        "season": season.title(),
        "climate": climate,
        "outfits": outfits,
        "total_outfits": len(outfits),
        "tips": tips,
        "summary": _build_summary(destination, days, outfits),
    }


def _build_summary(destination: str, days: int, outfits: List[Dict]) -> str:
    labels = [o["label"] for o in outfits]
    listed = ", ".join(f"1 {l.lower()}" for l in labels)
    return f"{days} day{'s' if days != 1 else ''} in {destination.title()}: {listed}."


def _get_packing_tips(climate: str, days: int) -> List[str]:
    base = [
        "Roll clothes instead of folding to save space.",
        "Pack a small laundry bag to separate worn items.",
        "Choose versatile neutral colours that mix and match easily.",
    ]
    climate_tips = {
        "hot":  ["Pack lightweight, breathable fabrics like linen and cotton.",
                 "A compact fan or cooling towel can be a lifesaver.",
                 "Sun protection: hat, sunglasses, and SPF are essential."],
        "warm": ["A light layer for evenings is always useful.",
                 "Breathable fabrics work well day-to-night."],
        "mild": ["Layering is key — mix and match tops with jackets.",
                 "A versatile trench coat covers most situations."],
        "cold": ["Thermal base layers maximise warmth without bulk.",
                 "Pack thermal socks and gloves if temperatures drop below 5°C.",
                 "A warm scarf doubles as a blanket on transit."],
    }
    tips = base + climate_tips.get(climate, [])
    if days >= 5:
        tips.append("For longer trips, plan 1–2 laundry sessions to re-wear key pieces.")
    return tips
