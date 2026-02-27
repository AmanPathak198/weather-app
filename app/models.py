from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime, timezone

class WeatherHistory(Base):
    __tablename__ = "weather_history"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    pressure = Column(Integer, nullable=False)
    condition = Column(String, nullable=False)
    searched_at = Column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc))
    # user_id = Column(Integer, ForeignKey())