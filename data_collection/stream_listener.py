import tweepy
import json

from database.db_operations import DbOperations


class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.
    def __init__(self, api=None):
        super(tweepy.StreamListener, self).__init__()
        self.is_recording = True
        self.search_params = None

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
        self.db_operations = DbOperations()

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        if not self.is_recording:  # check if stop streaming requested
            return False

        words = self.search_params['words']
        datajson = json.loads(data)

        if not datajson['retweeted'] and not datajson['text'].startswith('RT @') and datajson['lang'] == 'en':  # if not a retweet and an an english tweet
            tweet_text = datajson['text'].lower()
            has_search_key_word = False
            for word in words:
                if word.lower() in tweet_text:
                    has_search_key_word = True
                    break

            if has_search_key_word:  # chack if the tweet actually has drug name in it
                try:
                    self.db_operations.insert_tweet(data)
                    return data
                except Exception as e:
                    print(e)
