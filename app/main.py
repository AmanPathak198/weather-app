from fastapi import FastAPI
from routes import weather
import models
from database import engine

app = FastAPI()

app.include_router(weather.router)

models.Base.metadata.create_all(bind=engine)



