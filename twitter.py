import math
from typing import List
import time
import tweepy
from tweepy import Tweet
from . import secrets, constants

# Twitter API
auth = tweepy.OAuthHandler(secrets.TWITTER_API_KEY, secrets.TWITTER_API_KEY_SECRET)
auth.set_access_token(secrets.TWITTER_ACCESS_TOKEN, secrets.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def tweet_method_name(method_name: str) -> Tweet:
    last_tweet = None
    if (len(method_name) > constants.MAX_TWEET_LENGTH):
        last_tweet = api.update_status(status=method_name[0, constants.MAX_TWEET_LENGTH])
        remaining_method_name = method_name[constants.MAX_TWEET_LENGTH,]
        for i in range(math.ceil(len(remaining_method_name) / constants.MAX_TWEET_LENGTH)):
            last_tweet = api.update_status(status=remaining_method_name[constants.MAX_TWEET_LENGTH * i, constants.MAX_TWEET_LENGTH * (i + 1)], in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)
    else:
        last_tweet = api.update_status(status=method_name)
    return last_tweet


def tweet_repo_information(repo_name: str, last_tweet: Tweet) -> Tweet:
    found_in_repo_message = f"Found in repository {repo_name}"
    if (len(found_in_repo_message) > constants.MAX_TWEET_LENGTH):
        for i in range(math.ceil(len(found_in_repo_message) / constants.MAX_TWEET_LENGTH)):
            last_tweet = api.update_status(status=found_in_repo_message[constants.MAX_TWEET_LENGTH * i, constants.MAX_TWEET_LENGTH * (i + 1)], in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)
    else:
        last_tweet = api.update_status(status=found_in_repo_message, in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)
    return last_tweet


def tweet_method_names(method_names_and_file_paths: List[tuple], repo_name: str) -> None:
    for method_name_and_file_path in method_names_and_file_paths:
        try:
            last_tweet = tweet_method_name(method_name_and_file_path[0])
            last_tweet = tweet_repo_information(repo_name, last_tweet)
            print("\n\n*******************************************************************************************")
            print(f"Tweet created for method \"{method_name_and_file_path[0]}\" from repo {repo_name} in filePath {method_name_and_file_path[1]}. Last tweet object: {last_tweet}")
            print("*******************************************************************************************\n\n")
            time.sleep(5)
        except Exception as e:
            print(f"Couldn't generate tweet for method {method_name_and_file_path[0]} in repo {repo_name} due to {e}")