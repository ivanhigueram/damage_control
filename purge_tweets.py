#!/usr/bin/env python

from datetime import datetime, timedelta
import os

import tweepy


def purge_tweets(
    auth_dict, number_days_kept, do_not_delete_list, delete_tweets=True, dry_run=False
) -> None:
    """Purge tweets from timeline up to cutoff date

    This function calls all available tweets in the timeline and removes all the
    tweets after a cutoff date. The functions relies on the Twitter API V1
    calls.

    Args:
        - auth_dict dict: A dictionary with the Twitter API credentials. The
          dict must have four keys: API an ACCESS tokens and secrets.
        - number_days int: number of days to keep from datetime.utcnow(). If the
          function is executed today, and `number_days = 10`, then only tweets
          from the last 10 days will be kept.
        - do_not_delete_list list: A list with tweet IDs. These tweets won't be
          eliminated.
        - delete_tweets bool: If True, delete all the tweets. Else will just
          print some data.
        - dry_run bool: just as `delete_tweets`. If True it wont do any
          destructive calls, just print actions

    Returns:
        None
    """

    # Load all credentials to start the API
    consumer_key = auth_dict.get("API_KEY")
    consumer_secret = auth_dict.get("API_KEY_SECRET")
    access_token = auth_dict.get("ACCESS_TOKEN")
    access_token_secret = auth_dict.get("ACCESS_TOKEN_SECRET")

    # Instantiate API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Define cutoff date
    cutoff_date = datetime.utcnow() - timedelta(days=number_days_kept)

    if delete_tweets:
        print("Retrieving timeline tweets")
        timeline = tweepy.Cursor(api.user_timeline).items()

        deletion_count: int = 0
        ignored_count: int = 0

        for tweet in timeline:
            # where tweets are not in save list and older than cutoff date
            if tweet.id not in do_not_delete_list and tweet.created_at < cutoff_date:
                print(f"Deleting {tweet.id}: [{tweet.created_at}]")
                if not dry_run:
                    api.destroy_status(tweet.id)
                    deletion_count += 1
            else:
                ignored_count += 1

        print(f"Deleted {deletion_count} tweets, ignored {ignored_count}")
    else:
        print("Not deleting tweets")

    return None


if __name__ == "__main__":

    # Get credentials from box
    creds_dict = {
        "API_KEY": os.environ.get("API_KEY"),
        "API_KEY_SECRET": os.environ.get("API_KEY_SECRET"),
        "ACCESS_TOKEN": os.environ.get("ACCESS_TOKEN"),
        "ACCESS_TOKEN_SECRET": os.environ.get("ACCESS_TOKEN_SECRET"),
    }
    purge_tweets(
        number_days=360, auth_dict=creds_dict, delete_tweets=True, dry_run=False
    )
