import httpx
from config import WeatherAppKey, WeatherBaseURL
from fastapi import HTTPException

async def fetch_weather(city: str):
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

    return{
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "condition": data["weather"][0]["description"]
    }


