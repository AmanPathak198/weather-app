from fastapi import APIRouter, Depends
from database import get_db
from services.weather_service import fetch_weather, get_weather_history, create_report
from sqlalchemy.orm import Session
from models import WeatherHistory
from typing import Optional
import io
import csv
from fastapi.responses import StreamingResponse
import pandas as pd



router = APIRouter()

@router.get('/weather/report/excel')
async def download_weather_excel(db: Session = Depends(get_db)):
    data = await create_report(db)

    weather_data = []

    for w in data:
        weather_data.append({
            "ID": w.id,
            "City": w.city,
            "Temperature": w.temperature,
            "Condition": w.condition,
            "Created_at": w.searched_at
        })

    df = pd.DataFrame(weather_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name = "Weather Report")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":"attachments; filename=weather_report.xlsx"
        })


@router.get('/weather/report')
async def weather_report(db: Session = Depends(get_db)):
    data= await create_report(db)
    
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["ID", "City", "Temperature", "Condition", "Created_At"])
    for w in data:
        writer.writerow([
            w.id,
            w.city,
            w.temperature,
            w.condition,
            w.searched_at
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition":"aattachments; filename=weather_report.csv"}
    )


@router.get("/weather/{city}")
async def get_weather(city : str, db: Session = Depends(get_db)):
    return await fetch_weather(city, db)

# @router.get('/history')
# async def get_history(db: Session= Depends(get_db)):
#     return db.query(WeatherHistory).all()

@router.get('/history')
async def get_history(skip: int = 0, limit: int = 10, city: Optional[str] = None, db: Session= Depends(get_db)):
    return await get_weather_history(db, skip=skip, limit=limit, city = city)

