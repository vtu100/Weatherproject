# FastAPI Weather Information Server

This is a FastAPI server that provides weather information based on latitude and longitude. It fetches weather data such as humidity, pressure, temperature, maximum temperature, and minimum temperature from the OpenWeatherMap API.

## Features
- Retrieve weather information (Humidity, Pressure, Temperature, Max Temperature, Min Temperature).
- Get weather data based on geographic coordinates (latitude and longitude).

## Requirements

- Python 3.7 or higher
- OpenWeatherMap API key (sign up at https://openweathermap.org/)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/vtu100/Weatherproject.git
cd weather-api-fastapi
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Sign up for an API key at OpenWeatherMap and replace the placeholder in the code with your actual API key.
```python
API_KEY = 'your_openweathermap_api_key'
```

## Running the Server
To start the FastAPI server, run the following command:
```bash
uvicorn main:app --reload
```
This will start the server at http://127.0.0.1:8000/.

## Usage

You can make a GET request to the /weather endpoint by providing lat and lon as query parameters.

Example Request:
```bash
http://127.0.0.1:8000/weather?lat=37.7749&lon=-122.4194
```
Example Response::
```json
{
  "humidity": 72,
  "pressure": 1013,
  "temperature": 15.6,
  "max_temperature": 17.8,
  "min_temperature": 13.5
}
```