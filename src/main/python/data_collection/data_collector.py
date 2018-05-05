import tweepy
from data_collection.stream_listener import StreamListener


class DataCollector:
    def __init__(self, search_params, auth_keys):
        self.search_params = search_params
        self.auth_keys = auth_keys
        self.stream_listener = StreamListener()

    def get_streamer(self):
        auth = tweepy.OAuthHandler(self.auth_keys['consumer_key'], self.auth_keys['consumer_secret'])
        auth.set_access_token(self.auth_keys['access_token'], self.auth_keys['access_token_secret'])
        # Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
        listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
        streamer = tweepy.Stream(auth=auth, listener=listener)

        return streamer

    def run_collection(self):
        streamer = self.get_streamer()
        print("Tracking: " + str(self.search_params['words']))
        streamer.filter(track=self.search_params['words'])
