from fastapi import APIRouter, Depends
from database import get_db
from services.weather_service import fetch_weather, get_weather_history
from sqlalchemy.orm import Session
from models import WeatherHistory
from typing import Optional

router = APIRouter()

@router.get("/weather/{city}")
async def get_weather(city : str, db: Session = Depends(get_db)):
    return await fetch_weather(city, db)

# @router.get('/history')
# async def get_history(db: Session= Depends(get_db)):
#     return db.query(WeatherHistory).all()

@router.get('/history')
async def get_history(skip: int = 0, limit: int = 10, city: Optional[str] = None, db: Session= Depends(get_db)):
    return await get_weather_history(db, skip=skip, limit=limit, city = city)

