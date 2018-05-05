import json

from pymongo import MongoClient
from config import db_config


class DbOperations:

    def insert_tweet(self, tweet):
        client = MongoClient(db_config['host'], db_config['port'])

        # Use twitterdb database. If it doesn't exist, it will be created.
        db = client[db_config['database']]

        # Decode the JSON from Twitter
        datajson = json.loads(tweet)

        # grab the 'created_at' data from the Tweet to use for display
        created_at = datajson['created_at']

        # print out a message to the screen that we have collected a tweet
        print("Tweet collected at " + str(created_at))

        # insert the data into the mongoDB into a collection called twitter_search
        # if twitter_search doesn't exist, it will be created.
        db[db_config['collection']].insert(datajson)

