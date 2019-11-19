import tweepy
from data_collection.stream_listener import StreamListener


class DataCollector:
    def __init__(self, search_params, auth_keys):
        self.search_params = search_params
        self.auth_keys = auth_keys
        # Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
        self.stream_listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
        self.set_stream_listener_search_params()

    def get_streamer(self):
        auth = tweepy.OAuthHandler(self.auth_keys['consumer_key'], self.auth_keys['consumer_secret'])
        auth.set_access_token(self.auth_keys['access_token'], self.auth_keys['access_token_secret'])
        streamer = tweepy.Stream(auth=auth, listener=self.stream_listener)

        return streamer

    def run_collection(self):
        streamer = self.get_streamer()
        print("Tracking: " + str(self.search_params['words']))
        streamer.filter(track=self.search_params['words'])
        # streamer.filter(locations=['x1', 'y1', 'x2', 'y2'])
        # streamer.filter(locations=[108.63,-45.08,157.14,-9.10])
        # streamer.filter(locations=[-6.38,49.87,1.77,55.81])

    def stop_collection(self):
        self.stream_listener.is_recording = False

    def set_stream_listener_search_params(self):
        self.stream_listener.search_params = self.search_params