import json
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import sys
import warnings
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

warnings.simplefilter("ignore")

# Load city data from local file
with open('city.list.json', 'r', encoding='utf-8') as fin:
    city_list_data = json.load(fin)


# FastAPI server setup
app = FastAPI()


def find_city_by_name(city_list_data: List) -> pd.DataFrame:
    """
    Search for a city in the city list by name.
    """
    city_name = input('Please Enter a City or State Name: ').title()
    city_list_df = pd.DataFrame(city_list_data)
    return city_list_df[city_list_df['name'] == city_name]


def display_city_on_map(city_df: pd.DataFrame, zoom_level: int = 3):
    """
    Display the city coordinates on a map using folium.
    """
    if len(city_df) == 0:
        print("City not found!")
        return

    city_coords = city_df['coord'].iloc[0]
    city_map = folium.Map(location=[city_coords['lat'], city_coords['lon']], zoom_start=zoom_level)

    for _, row in city_df.iterrows():
        coords = [row['coord']['lat'], row['coord']['lon']]
        city_id = str(row['id'])
        folium.Marker(coords, popup=city_id).add_to(city_map)

    return city_map


def get_city_coordinates_from_user(city_df: pd.DataFrame):
    """
    Prompt the user to select a city ID from the displayed map and get the city coordinates.
    """
    city_id = int(input('Click on the location, and Enter the city ID: '))
    city_data = city_df[city_df['id'] == city_id]
    if city_data.empty:
        sys.exit('City ID not recognized. Please restart the program.')
    return city_data['coord'].values[0]


def get_weather_data_from_api(lat: float, lon: float) -> pd.DataFrame:
    """
    Fetch weather data from the FastAPI weather endpoint.
    """
    # Making GET request to the FastAPI server (assumed running locally)
    response = requests.get(f'http://127.0.0.1:8000/weather?lat={lat}&lon={lon}')
    return pd.DataFrame([response.json()])


def generate_weather_map(weather_df: pd.DataFrame) -> folium.Map:
    """
    Generate a folium map to visualize the weather data.
    The map center will be determined from the coordinates of the first city in weather_df.
    """
    # Extract the coordinates from the weather_df (assuming it's a single entry or the first one)
    first_entry = weather_df.iloc[0]
    city_coords = [first_entry['lat'], first_entry['lon']]
    
    # Set the map center to the first city's coordinates
    map_obj = folium.Map(location=city_coords, zoom_start=7)
    
    # Create a MarkerCluster to handle multiple markers on the map
    marker_cluster = MarkerCluster().add_to(map_obj)

    # Add each weather entry to the map
    for row in weather_df.to_records():
        coords = (row['lat'], row['lon'])
        info = (
            f"{row['name']} ||| "
            f"Humidity: {row['humidity']}  "
            f"Pressure: {row['pressure']}  "
            f"Temp: {row['temperature']}°C  "
            f"Max Temp: {row['max_temperature']}°C  "
            f"Min Temp: {row['min_temperature']}°C"
        )
        color = get_marker_color(row)
        folium.CircleMarker(
            location=coords, radius=15, popup=info, color=color, fill_color=color
        ).add_to(marker_cluster)

    return map_obj

def get_marker_color(row) -> str:
    """
    Get the color based on temperature.
    """
    temp = row['temperature']
    if temp >= 35:
        return '#840319'
    elif temp >= 30:
        return '#e51b1b'
    elif temp >= 25:
        return '#e5791b'
    elif temp >= 20:
        return '#e5b91b'
    elif temp >= 15:
        return '#eae71c'
    elif temp >= 10:
        return '#94ff42'
    elif temp >= 5:
        return '#34f474'
    elif temp >= 0:
        return '#34f4d4'
    elif temp >= -5:
        return '#7ccdff'
    elif temp >= -10:
        return '#7972ff'
    elif temp >= -15:
        return '#3c15c6'
    else:
        return '#64259b'


def main():
    # Fetch the city by name
    city_df = find_city_by_name(city_list_data)
    display_city_on_map(city_df)

    try:
        city_coords = get_city_coordinates_from_user(city_df)
    except ValueError:
        sys.exit('Invalid city ID entered, please restart the program.')

    lat, lon = city_coords['lat'], city_coords['lon']
    weather_df = get_weather_data_from_api(lat, lon)
    generate_weather_map(weather_df)


if __name__ == "__main__":
    main()
