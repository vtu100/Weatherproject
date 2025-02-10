from fastapi import FastAPI
import httpx
from pydantic import BaseModel
from typing import Dict

# Define your OpenWeatherMap API key and base URL
API_KEY = 'a25d1d829017939bed74839d6b73f55f'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

app = FastAPI()

class WeatherResponse(BaseModel):
    name: str
    lat: float
    lon: float
    humidity: float
    pressure: float
    temperature: float
    max_temperature: float
    min_temperature: float

@app.get("/weather", response_model=WeatherResponse)
async def get_weather(lat: float, lon: float):
    # Make a request to OpenWeatherMap API
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',  # Temperature in Celsius
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        data = response.json()

    # Extract weather data from the response
    weather_data = WeatherResponse(
        name=data['name'],
        lat=lat,
        lon=lon,
        humidity=data['main']['humidity'],
        pressure=data['main']['pressure'],
        temperature=data['main']['temp'],
        max_temperature=data['main']['temp_max'],
        min_temperature=data['main']['temp_min']
    )

    return weather_data
