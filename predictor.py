import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from weather import get_weather, convert_weather_to_df, get_past_weather, extract_temp_values


def calculate_z_score(new_value: float, historical_values: pd.Series)->float:
    """Returns a z-score for a new value based on a series of historical values"""
    mean = np.mean(historical_values)
    std_dev = np.std(historical_values, ddof=0)
    z_score = (new_value - mean) / std_dev
    return z_score


def get_latitude_longitude(team_name:str, stadium_locations:pd.DataFrame):
    """Returns the latitude and longitude of a given team's stadium"""
    lat = stadium_locations[stadium_locations['team_name'] == team_name]['lat'].iloc[0]
    lon = stadium_locations[stadium_locations['team_name'] == team_name]['long'].iloc[0]
    return lat, lon


def calculate_team_z_score(team_name: str, game_id: str, game_time_temp: float, stadium_locations: pd.DataFrame, start_date: str, end_date: str) -> dict:
    """
    Helper function to calculate the z-score for a given team
    Returns a dictionary with the game_id, team_name, and z_score
    """
    lat, lon = get_latitude_longitude(team_name, stadium_locations)
    past_weather = get_past_weather(lat, lon, start_date, end_date)
    past_weather_temps = extract_temp_values(past_weather)
    z_score = calculate_z_score(game_time_temp, past_weather_temps)

    return {
        'game_id': game_id,
        'team_name': team_name,
        'z_score': z_score
    }


def process_z_scores(odds:dict, stadium_locations:pd.DataFrame)->list:
    """
    Takes in the slate of games and the stadium locations and returns the z-scores for each team in each game.
    The z-score is calculated based on the temperature at game time and the historical temperatures for the team's city.
    This function is suppose to answer the question: 
    "How much out of the ordinary is the temperature for this game for this team?"

    Args:
        odds (dict): The slate of games for a given Sunday on the odds API
        stadium_locations (pd.DataFrame): A DataFrame with the stadium locations for each NFL team

    Returns:
        list: A list of dictionaries with the game_id, team_name, and z_score for each dictionary
    """
    end_date = datetime.now().strftime('%Y-%m-%dT00:00:00')
    # We will calculate "historical temperatures" by looking at the past 30 days
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT00:00:00')
    results = []

    for game in odds:
        game_id = game['id']
        home_team = game['home_team']
        away_team = game['away_team']
        game_time = game['commence_time']

        roof_type = stadium_locations[stadium_locations['team_name'] == home_team]['roof'].iloc[0]
        if roof_type in ['yes','retractable']:
            continue
        
        home_city = stadium_locations[stadium_locations['team_name'] == home_team]['City'].iloc[0]
        weather = get_weather(home_city)
        weather_df = convert_weather_to_df(weather)
        game_time_temp = weather_df.loc[(weather_df['Timestamp'] - game_time).abs().idxmin()]['Temperature']

        results.append(calculate_team_z_score(home_team, game_id, game_time_temp, stadium_locations, start_date, end_date))
        results.append(calculate_team_z_score(away_team, game_id, game_time_temp, stadium_locations, start_date, end_date))


    return results
