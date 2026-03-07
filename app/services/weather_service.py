import httpx
from config import WeatherAppKey, WeatherBaseURL
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models import WeatherHistory

async def fetch_weather(city: str, db: Session):
    params = {
        "q": city,
        "appid": WeatherAppKey,
        "units": "metric"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(WeatherBaseURL, params= params)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail = "City not found")
    
    if response.status_code != 200:
        raise HTTPException(status_code= 500, detail="Weather API Error")
    
    data = response.json()

    weather_record = WeatherHistory(
        city = data["name"],
        temperature= data["main"]["temp"],
        humidity= data["main"]["humidity"],
        pressure= data["main"]["pressure"],
        condition= data["weather"][0]["description"]
    )

    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)

    return{
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "condition": data["weather"][0]["description"]
    }


async def get_weather_history(db: Session, skip:int = 0, limit: int = 10, city: str | None = None ):
    query = db.query(WeatherHistory)

    if city:
        query = query.filter(WeatherHistory.city == city)
    return query.offset(skip).limit(limit).all()
