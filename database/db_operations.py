import json
from dateutil.parser import parse

from pymongo import MongoClient, DESCENDING
from settings import DB_SETTINGS as db_config


class DbOperations:
    def __init__(self):
        self.client = MongoClient(db_config['host'], db_config['port'])
        self.db = self.client[db_config['database']]
        self.online_collection = self.db[db_config['collection']]

    def insert_tweet(self, tweet):

        # Decode the JSON from Twitter
        datajson = json.loads(tweet)

        # grab the 'created_at' data from the Tweet to use for display

        if not datajson['retweeted'] and not datajson['text'].startswith('RT @') and datajson['lang'] == 'en':
            datajson['created_at'] = parse(datajson['created_at']).timestamp()
            insert_id = self.online_collection.insert(datajson)
            print("Tweet collected with id " + str(insert_id))

    def get_last_tweet(self):
        return self.online_collection.find_one({}, sort=[('_id', DESCENDING)])