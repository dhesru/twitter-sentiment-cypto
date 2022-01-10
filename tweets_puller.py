import os
import tweepy
import pandas as pd
import json
from datetime import datetime
from dateutil import tz
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


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
tweets = api.user_timeline(screen_name='danielesesta',count=5000,include_rts=False)
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
    for k_c_w in key_crypto_words:
        if k_c_w in tweet_ori:
            tweets_dict['tweet'].append(tweet_ori)
            tweets_dict['created_at'].append(tweet_created)


tweets_data = pd.DataFrame.from_dict(tweets_dict)

sentences = tweets_data['tweet']

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

analyze_dict = dict()
analyze_dict['neg'] = list()
analyze_dict['neu'] = list()
analyze_dict['pos'] = list()
analyze_dict['compound'] = list()
analyze_dict['created_at'] = list()

count = 0
for twt in tweets_dict.get('tweet'):
    created_at = tweets_dict.get('created_at')[count]
    vs = analyzer.polarity_scores(twt)
    analyze_dict['neg'].append(vs.get('neg'))
    analyze_dict['neu'].append(vs.get('neu'))
    analyze_dict['pos'].append(vs.get('pos'))
    analyze_dict['compound'].append(vs.get('compound'))
    analyze_dict['created_at'].append(created_at)
    count += 1

analyze_df = pd.DataFrame.from_dict(analyze_dict)
analyze_df = analyze_df.set_index('created_at')

print(analyze_df)

sns.set(rc={'figure.figsize':(11, 4)})

cols_plot = ['neg','neu','pos','compound']
axes = analyze_df[cols_plot].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9), subplots=True)
cnt = 0
for ax in axes:
    y_label = 'Plot for ' + str(cols_plot[cnt])
    ax.set_ylabel(y_label)
    ax.set_ylim(-1.2,1.2)
    cnt += 1
plt.show()
