import pandas as pd
from sqlalchemy import create_engine


if __name__ ==  "__main__":
    
    con = create_engine('sqlite:///backups/purged_tweet_db.sql')
    df: pd.DataFrame = pd.read_sql("""
    SELECT strftime('%Y', date(created_at)) as year, 
    retweeted, 
    count(*) as count
    FROM tweets
    GROUP BY strftime('%Y', date(created_at)), retweeted;
    """, con=con)
    df.to_json('backups/year_groupby.json', orient='records')

