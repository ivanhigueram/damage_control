#!/usr/bin/env python

from datetime import datetime, timedelta
import os

from sqlalchemy import create_engine

import pandas as pd
import tweepy


def purge_tweets(
    auth_dict, number_days_kept, do_not_delete_list, dry_run=False, back_up=False
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
        - dry_run bool: If `True` it wont do any destructive calls, just print
          actions
        - back_up bool: If `True` appends the timeline to a SQLite database

    Returns:
        None
    """

    # Load all credentials to start the API
    consumer_key: str = auth_dict.get("API_KEY")
    consumer_secret: str = auth_dict.get("API_KEY_SECRET")
    access_token: str = auth_dict.get("ACCESS_TOKEN")
    access_token_secret: str = auth_dict.get("ACCESS_TOKEN_SECRET")

    # Instantiate API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Define cutoff date
    cutoff_date = datetime.utcnow() - timedelta(days=number_days_kept)

    print("Retrieving timeline tweets")
    timeline = tweepy.Cursor(api.user_timeline, tweet_mode="extended").items()

    deletion_count: int = 0
    ignored_count: int = 0

    tweets_lst = []
    for tweet in timeline:
        # where tweets are not in save list and older than cutoff date
        if (
            tweet.id not in do_not_delete_list
            and tweet.created_at.replace(tzinfo=None) < cutoff_date
        ):
            print(f"Deleting {tweet.id}: [{tweet.created_at}]")
            if not dry_run:
                api.destroy_status(tweet.id)
                deletion_count += 1
                tweets_lst.append(tweet)
        else:
            ignored_count += 1

    print(f"Deleted {deletion_count} tweets, ignored {ignored_count}")

    # Back up tweets in dict/json
    cols = [
        "created_at",
        "id",
        "id_str",
        "full_text",
        "in_reply_to_screen_name",
        "is_quote_status",
        "favorited",
        "retweeted",
    ]

    if back_up:
        df_tweets: pd.DataFrame = pd.DataFrame([t._json for t in tweets_lst])
        try:
            df_tweets_subset = df_tweets[cols]
        except KeyError:
            raise RuntimeError("Column subset not working!")

        if not os.path.exists("./backups"):
            os.makedirs("./backups")
            con = create_engine("sqlite://backups/purged_tweet_db.sql")
        else:
            # Avoid repetition in DB -- ideally this could be solved on the SQL
            # side, but no time.
            con = create_engine("sqlite:///backups/purged_tweet_db.sql")
            ids: pd.DataFrame = pd.read_sql("SELECT DISTINCT id FROM tweets", con=con)
            df_tweets_subset: pd.DataFrame = df_tweets_subset[
                ~df_tweets_subset["id"].isin(ids["id"].tolist())
            ]

        rows: int = df_tweets_subset.to_sql(
            "tweets", con=con, index=False, if_exists="append"
        )

        print(f"Updated {rows} rows in the SQL database")

    return None


if __name__ == "__main__":

    # Get credentials from box
    creds_dict = {
        "API_KEY": os.environ.get("API_KEY"),
        "API_KEY_SECRET": os.environ.get("API_KEY_SECRET"),
        "ACCESS_TOKEN": os.environ.get("ACCESS_TOKEN"),
        "ACCESS_TOKEN_SECRET": os.environ.get("ACCESS_TOKEN_SECRET"),
    }

    # Keep tweets
    list_keep = ["1418600894644461569"]
    purge_tweets(
        number_days_kept=360,
        auth_dict=creds_dict,
        do_not_delete_list=list_keep,
        dry_run=True,
        back_up=True
    )
