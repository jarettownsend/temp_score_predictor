from odds import main as odds_main
from predictor import process_z_scores
import pandas as pd

def main():
    odds = odds_main()
    stadium_locations = pd.read_csv('nfl_stadium_locations.csv')
    z_scores = process_z_scores(odds, stadium_locations)
    max_z_score_dict = max(z_scores, key=lambda x: abs(x['z_score']))

    # Will need to get the information we want from odds.
    # The team most out of their element should be bet against
    # Will post this info on Twitter

    return max_z_score_dict
