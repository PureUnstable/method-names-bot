import logging
import sys
import math
from typing import List
import time
import tweepy
from tweepy import Tweet
import secrets, constants


# Twitter API
auth = tweepy.OAuthHandler(secrets.TWITTER_API_KEY, secrets.TWITTER_API_KEY_SECRET)
auth.set_access_token(secrets.TWITTER_ACCESS_TOKEN, secrets.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def tweet_spooler(tweet_message: str, last_tweet: Tweet) -> Tweet:
    for i in range(math.ceil(len(tweet_message) / constants.MAX_TWEET_LENGTH)):
        if i is 0 and last_tweet is None:
            last_tweet = api.update_status(status=tweet_message[(constants.MAX_TWEET_LENGTH * i): (constants.MAX_TWEET_LENGTH + (constants.MAX_TWEET_LENGTH * i))])
        else:
            last_tweet = api.update_status(status=tweet_message[(constants.MAX_TWEET_LENGTH * i): (constants.MAX_TWEET_LENGTH + (constants.MAX_TWEET_LENGTH * i))], in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)
        time.sleep(5)
    return last_tweet

def tweet_method_name(method_name: str) -> Tweet:
    last_tweet = tweet_spooler(method_name, None)
    return last_tweet


def tweet_repo_information(repo_name: str, last_tweet: Tweet) -> Tweet:
    repo_info = f"Found in repository {repo_name}"
    last_tweet = tweet_spooler(repo_info, last_tweet)
    return last_tweet


def tweet_method_names(method_names: List[str], repo_name: str) -> None:
    for method_name in method_names:
        try:
            last_tweet = tweet_method_name(method_name)
            last_tweet = tweet_repo_information(repo_name, last_tweet)
            logging.info("\n\n*******************************************************************************************" +
                        f"Tweet created for method \"{method_name}\" from repo {repo_name}" +
                         "*******************************************************************************************\n\n"
            )
        except Exception as e:
            logging.error(f"Couldn't generate tweet for method {method_name} in repo {repo_name} due to {e}")

if __name__ == "__main__":
    tweet_method_names(["Hello"], "World")