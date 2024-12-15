from odds import main as odds_main
from predictor import process_z_scores
import pandas as pd

def create_tweet(max_z_score_dict):
    # We should probably add what the line is in here
    # Also we should spice up these tweets. More of a placeholder for now
    if max_z_score_dict['z_score'] > 0:
        return f"Bet against the {max_z_score_dict['team_name']}. They won't be able to handle the heat"
    if max_z_score_dict['z_score'] < 0:
        return f"Bet against the {max_z_score_dict['team_name']}. They won't be able to handle the cold"


def main():
    odds = odds_main()
    stadium_locations = pd.read_csv('nfl_stadium_locations.csv')
    z_scores = process_z_scores(odds, stadium_locations)
    max_z_score_dict = max(z_scores, key=lambda x: abs(x['z_score']))
    tweet = create_tweet(max_z_score_dict)
    # Will post this info on Twitter

    return tweet
