# Download Tweets Using Twitter API

### Install MongoDb 
Follow the instructions here
```
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
```
### Install python packages 
Run the command
```
pip install -r requirements.txt 
```
### App Settings
In the settings file, write your twitter app credentials in the AUTH_SETTINGS dictionary. 
```
AUTH_SETTINGS = {
    # app: hk-twitter-data-mining
    'consumer_key': "####",
    'consumer_secret': "####",
    'access_token': "####",
    'access_token_secret': "####",
}
```

Optionally, you can change database name and collection name in the DB_settings dictionary.

```
DB_SETTINGS = {
    'host': 'localhost',
    'port': 27017,
    'database': 'twitter_db',  # if does not exist, will be created automatically
    'collection': 'twitter_data'  # if does not exist, will be created automatically
}
``` 

### Start Downloading tweets
Run the following command
```
python download_tweets.py
```

### Export Tweets
Run the following command to export tweets as csv
```
mongoexport --db climate_adaptation_db --collection ca_data --type=csv --fields id_str,text,extended_tweet.full_text --out tweets.csv
```

Run the following command to export tweets as json
```
mongoexport --db climate_adaptation_db --collection ca_data --type=json --out tweets.json
```
