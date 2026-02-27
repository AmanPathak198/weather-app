from fastapi import APIRouter, Depends
from database import get_db
from services.weather_service import fetch_weather
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/weather/{city}")
async def get_weather(city : str, db: Session = Depends(get_db)):
    return await fetch_weather(city, db)