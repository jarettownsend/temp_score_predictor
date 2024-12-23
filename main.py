from odds import main as odds_main
from predictor import process_z_scores
from posting_x import post_to_x
import pandas as pd

def create_tweet(odds, max_z_score_dict):
    for game in odds:
        if game['id'] != max_z_score_dict['game_id']:
            continue
        else:
            if game['projected_winner'] == max_z_score_dict['team_name']:
                return (
                    f"Predicting the {max_z_score_dict['team_name']} to win "
                    f"by less than {game['projected_spread']} points"
                )
            elif game['projected_winner'] != max_z_score_dict['team_name']:
                return (
                    f"Predicting the {max_z_score_dict['team_name']} to lose "
                    f"by more than {game['projected_spread']} points"
                )


def main():
    odds = odds_main()
    stadium_locations = pd.read_csv('nfl_stadium_locations.csv')
    z_scores = process_z_scores(odds, stadium_locations)
    max_z_score_dict = max(z_scores, key=lambda x: abs(x['z_score']))
    tweet = create_tweet(odds, max_z_score_dict)
    post_to_x(tweet=tweet)


if __name__ == "__main__":
    main()