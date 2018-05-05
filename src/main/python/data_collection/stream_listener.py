import tweepy

from database.db_operations import DbOperations

class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
        self.db_operations = DbOperations()

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        try:
            self.db_operations.insert_tweet(data)
            return data
        except Exception as e:
            print(e)