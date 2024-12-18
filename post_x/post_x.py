import os
import tweepy
from requests_oauthlib import OAuth1
import requests
from dotenv import load_dotenv
load_dotenv()

# https://developer.x.com/en/portal/projects/1859377956109389824/apps/29645721/keys



def create_tweet():
    return "Hello World!"

def post_to_x():
    # Authenticate to Twitter
    """
    auth = tweepy.OAuth1UserHandler(os.environ["X_API_KEY"],
                                    os.environ["X_API_KEY_SECRET"],
                                    os.environ["X_ACCESS_TOKEN"],
                                    os.environ["X_ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth)

    # Create a tweet
    tweet = create_tweet()

    try:
        api.update_status(tweet)
        print("Tweet posted successfully!")
    except Exception as e:
        print("Error posting tweet: ", e)
    """
    url = 'https://api.x.com/2/tweets'
    auth = OAuth1(os.environ["X_API_KEY"],
                  os.environ["X_API_KEY_SECRET"],
                  os.environ["X_ACCESS_TOKEN"],
                  os.environ["X_ACCESS_TOKEN_SECRET"])
    payload = {
        "text": create_tweet()
    }
    response = requests.post(url, json=payload, auth=auth)

    if response.status_code == 200:
        print("Tweet posted successfully!")
    else:
        print("Error posting tweet: ", response.text)


if __name__ == "__main__":
    post_to_x()