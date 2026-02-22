from fastapi import APIRouter

from services.weather_service import fetch_weather

router = APIRouter()

@router.get("/weather/{city}")
async def get_weather(city : str):
    return await fetch_weather(city)