import os
import tweepy
import pandas as pd
import json
from datetime import datetime
from dateutil import tz

# access_token= '313172786-mGNKBZ3a2yqx5MEIzpp8e0kGRkmkgqT7FC7uBRNV'
# access_token_secret= 'P9ZRGItNdQmesvwY70hCf3NcSrbemZ4wkeuXk6G1DZLvm'
# consumer_key = 'MSiAIRflflPUv8kHmzsRsTU9t'
# consumer_secret = 'GFKLg2EL4S6xfuMoiiY5IoyoL7W9Ep7DAJP2tEQED6JMt7DWV5'

bearer_token = 'AAAAAAAAAAAAAAAAAAAAALIA9QAAAAAAlr6qZhJQvLWKbUHMsCw4cPWK28c%3Dgfj4qlTc0uRShQoeBazbKgNLzZCz7E9HkIztBI2P7ZPfGwhORs'

cwd = os.getcwd()
json_file_path = cwd + "/" + "creds.json"

with open(json_file_path) as json_file:
    json_data = json.load(json_file)

access_token = json_data.get('access_token')
access_token_secret = json_data.get('access_token_secret')
consumer_key = json_data.get('consumer_key')
consumer_secret = json_data.get('consumer_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Get the User object for twitter...
tweets = api.user_timeline(screen_name='danielesesta',count=100)
to_zone = tz.gettz('Asia/Singapore')

tweets_df = pd.DataFrame()
tweets_dict = dict()
tweets_dict['tweet'] = list()
tweets_dict['created_at'] = list()

# https://www.nasdaq.com/articles/decoding-crypto%3A-top-25-crypto-terms-you-need-to-know-2021-09-13
key_crypto_words = ['address','altcoin','bitcoin','eth','sol','blockchain','btfd','dapps','defi','fiat','fork','gas','halving','hash rate','hodl',
                    'ico','mining','nft','pump and dump', 'satoshi','stablecoin','token','to the moon','rekt','wallet','whale','dip']

for tweet in tweets:
    tweet_ori = tweet._json.get('text')
    tweet_created = tweet._json.get('created_at')
    tweet_created = datetime.strptime(tweet_created,'%a %b %m %H:%M:%S %z %Y').astimezone(to_zone)
    tweets_dict['tweet'].append(tweet_ori)
    tweets_dict['created_at'].append(tweet_created)


tweets_data = pd.DataFrame.from_dict(tweets_dict)

sentences = tweets_data['tweet']

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence)
    print("{:-<65} {}".format(sentence, str(vs)))


