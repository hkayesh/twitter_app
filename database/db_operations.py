import json
from dateutil.parser import parse

from pymongo import MongoClient, DESCENDING
from settings import DB_SETTINGS as db_config


class DbOperations:
    def __init__(self):
        self.client = MongoClient(db_config['host'], db_config['port'])
        self.db = self.client[db_config['database']]
        self.collection = self.db[db_config['collection']]

    def insert_tweet(self, tweet):

        # Decode the JSON from Twitter
        datajson = json.loads(tweet)

        # grab the 'created_at' data from the Tweet to use for display

        if not datajson['retweeted'] and not datajson['text'].startswith('RT @') and datajson['lang'] == 'en':
            print("A new tweet collected at " + datajson['created_at'])
            datajson['created_at'] = parse(datajson['created_at']).timestamp()

            # insert the data into the mongoDB into a collection called twitter_search
            # if twitter_search doesn't exist, it will be created.
            self.collection.insert(datajson)

    def get_last_tweet(self):
        return self.collection.find_one({}, sort=[('_id', DESCENDING)])
