import requests
import json
import os
import time
from dotenv import load_dotenv
load_dotenv()


api_key = os.environ["ODDS_API_KEY"]
sport_key= "americanfootball_nfl"
REGIONS = 'us'
MARKETS = 'spreads'
ODDS_FORMAT = 'decimal' # decimal | american
DATE_FORMAT = 'unix'
BOOK_MAKER = 'fanduel'

def sunday_date():
    sunday = time.localtime(time.time() + (6 - time.localtime().tm_wday) * 86400)
    return time.strftime('%Y-%m-%d', sunday)+'T00:00:00Z'

def monday_date():
    monday = time.localtime(time.time() + (7 - time.localtime().tm_wday) * 86400)
    return time.strftime('%Y-%m-%d', monday)+'T00:00:00Z'

def pull_odds_data() -> json:
    try:
        odds_response = requests.get(
            f'https://api.the-odds-api.com/v4/sports/{sport_key}/odds',
            params={
                'api_key': api_key,
                'regions': REGIONS,
                'markets': MARKETS,
                'oddsFormat': ODDS_FORMAT,
                'dateFormat': DATE_FORMAT,
                'commenceTimeFrom': sunday_date(),
                'commenceTimeTo': monday_date(),
            }
        )
        return odds_response.json()
    except requests.exceptions.RequestException as e:
        print('Error in pull_odds_data: ', e)
        raise Exception(e)


def clean_odds_data(odds_data: json):
    try:
        clean_odds_data__list = []
        for row in odds_data:
            clean_odds_data = {}
            clean_odds_data['id'] = row['id']
            clean_odds_data['commence_time'] = row['commence_time']
            clean_odds_data['home_team'] = row['home_team']
            clean_odds_data['away_team'] = row['away_team']
            for bookmaker in row['bookmakers']:
                if bookmaker['key'] == BOOK_MAKER:
                    for odds in bookmaker['markets'][0]['outcomes']:
                        if odds['point'] < 0:
                            clean_odds_data['projected_winner'] = odds['name']
                            clean_odds_data['projected_spread'] = abs(odds['point'])
                        elif odds['point'] == 0:
                            clean_odds_data['projected_winner'] = 'Tie'
                            clean_odds_data['projected_spread'] = 0
            clean_odds_data__list.append(clean_odds_data)
        return clean_odds_data__list

    except Exception as e:
        print('Error in clean_odds_data: ', e)
        raise Exception(e)

def main():
    try:
        odds_data = pull_odds_data()
        clean_data = clean_odds_data(odds_data)
        return clean_data
    except Exception as e:
        print('Error in main: ', e)
        raise Exception(e)
