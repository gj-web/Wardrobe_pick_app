"""
Wardrobe Pick — Main Application Entry Point
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import outfit, wardrobe

app = FastAPI(
    title="Wardrobe Pick",
    description="AI-powered capsule wardrobe planner for travel",
    version="2.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(outfit.router)
app.include_router(wardrobe.router)
