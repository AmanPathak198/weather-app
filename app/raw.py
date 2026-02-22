import requests
import datetime as dt
from config import WeatherBaseURL, WeatherAppKey

CITY = "London"

#https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API key}

url = WeatherBaseURL + "?" + "appid=" + WeatherAppKey + "&q=" + CITY

response = requests.get(url).json()

print(response)

temp = response['main']['temp']
print(temp)