import requests
import logging
from datetime import datetime
import pandas as pd


def get_weather(city, api_key):
    """
    Get the 3 day weather forecast for a city from the OpenWeatherMap API
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logging.error(f"Failed to get data: {response.status_code}")
        return None


def kelvin_to_fahrenheit(kelvin_temp):
    fahrenheit_temp = (kelvin_temp - 273.15) * 9 / 5 + 32
    return fahrenheit_temp


def convert_weather_to_df(future_weather):
    """
    Converts the weather data from the OpenWeatherMap API from JSON format into a pandas DataFrame
    """

    timestamps = []
    readable_times = []
    temperatures = []
    descriptions = []

    for entry in future_weather["list"]:
        timestamp = entry["dt"]
        readable_time = datetime.fromtimestamp(timestamp)
        temperature = kelvin_to_fahrenheit(entry["main"]["temp"])
        weather_description = entry["weather"][0]["description"]

        timestamps.append(timestamp)
        readable_times.append(readable_time)
        temperatures.append(temperature)
        descriptions.append(weather_description)

    weather_df = pd.DataFrame(
        {
            "Timestamp": timestamps,
            "Readable Time": readable_times,
            "Temperature": temperatures,
            "Description": descriptions,
        }
    )

    return weather_df
