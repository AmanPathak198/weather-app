from dotenv import load_dotenv
import os

load_dotenv()

WeatherAppKey = os.getenv('WEATHER_API_KEY')
WeatherBaseURL = os.getenv('BASE_WEATHER_URL')

if WeatherAppKey is None:
    raise ValueError("Key is not set in environment.")