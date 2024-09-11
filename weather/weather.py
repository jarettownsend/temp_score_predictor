import requests
import logging
from datetime import datetime
import pandas as pd
import os


def get_weather(city):
    """
    Get the 3 day weather forecast for a city from the OpenWeatherMap API
    """
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={os.environ["OPENWEATHERMAP_API_KEY"]}'
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


def convert_past_weather_to_df(past_weather):
    data = []
    for data_ in past_weather['locations'].values():
        data.extend(data_['values']) 
    
    df = pd.DataFrame(data)
    
    return df

def get_past_weather(lon, lat, start_date, end_date):
    """
    Get historical weather data for a specific location and time.
    """
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?&aggregateHours=24&startDateTime={start_date}&endDateTime={end_date}&unitGroup=us&contentType=json&dayStartTime=0:0:00&dayEndTime=0:0:00&location={lon},{lat}&key={os.environ["VISUALCROSSING_API_KEY"]}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logging.error(f"Failed to get data: {response.status_code}")
        return None