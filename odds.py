import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


api_key = os.environ["ODDS_API_KEY"]
sport_key= "americanfootball_nfl"
REGIONS = 'us'
MARKETS = 'spreads'
ODDS_FORMAT = 'decimal' # decimal | american
DATE_FORMAT = 'unix'

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{sport_key}/odds',
    params={
        'api_key': api_key,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

with open('odds_response.json', 'w', encoding='utf-8') as f:
    json.dump(odds_response.json(), f, ensure_ascii=False, indent=4)