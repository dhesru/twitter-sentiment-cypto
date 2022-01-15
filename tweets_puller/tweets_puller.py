import os
import tweepy
import pandas as pd
import json
from datetime import datetime
from dateutil import tz
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
tweets = api.user_timeline(screen_name='danielesesta',count=100,include_rts=False)
to_zone = tz.gettz('Asia/Singapore')

tweets_df = pd.DataFrame()
tweets_dict = dict()
tweets_dict['tweet'] = list()
tweets_dict['created_at'] = list()

# https://www.nasdaq.com/articles/decoding-crypto%3A-top-25-crypto-terms-you-need-to-know-2021-09-13
key_crypto_words = ['address','altcoin','bitcoin','eth','sol','blockchain','btfd','dapps','defi','fiat','fork','gas','halving','hash rate','hodl',
                    'ico','mining','nft','pump and dump', 'satoshi','stablecoin','token','to the moon','rekt','wallet','whale','dip','crypto']

key_token_words = ['ice','spell','time','solid']

class FilterTweets():
    analyze_dict = dict()
    analyze_dict['neg'] = list()
    analyze_dict['neu'] = list()
    analyze_dict['pos'] = list()
    analyze_dict['compound'] = list()
    analyze_dict['created_at'] = list()
    analyze_dict['tweet'] = list()

    tweets_dict = dict()
    tweets_dict['tweet'] = list()
    tweets_dict['created_at'] = list()


    def filter_tweets_by_wrds(self,filter_words,tweets):
        for tweet in tweets:
            tweet_ori = tweet._json.get('text')
            tweet_created = tweet._json.get('created_at')
            tweet_created = datetime.strptime(tweet_created,'%a %b %d %H:%M:%S %z %Y').astimezone(to_zone)
            for f_w in filter_words:
                if f_w in tweet_ori:
                    self.tweets_dict['tweet'].append(tweet_ori)
                    self.tweets_dict['created_at'].append(tweet_created)

            tweets_df = pd.DataFrame.from_dict(self.tweets_dict)
            sentences = tweets_df['tweet']
        return self.tweets_dict

    def get_sentiments(self,tweets_dict):
        if len(tweets_dict) > 0:
            count = 0
            analyzer = SentimentIntensityAnalyzer()
            for twt in tweets_dict.get('tweet'):
                created_at = tweets_dict.get('created_at')[count]
                vs = analyzer.polarity_scores(twt)
                self.analyze_dict['tweet'].append(twt)
                self.analyze_dict['neg'].append(vs.get('neg'))
                self.analyze_dict['neu'].append(vs.get('neu'))
                self.analyze_dict['pos'].append(vs.get('pos'))
                self.analyze_dict['compound'].append(vs.get('compound'))
                self.analyze_dict['created_at'].append(created_at)
                count += 1

            return self.analyze_dict

                # analyze_df = pd.DataFrame.from_dict(self.analyze_dict)
                # analyze_df = analyze_df.set_index('created_at')
                #
                # sns.set(rc={'figure.figsize': (11, 4)})
                #
                # cols_plot = ['neg', 'neu', 'pos', 'compound']
                # axes = analyze_df[cols_plot].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9), subplots=True)
                # cnt = 0
                # for ax in axes:
                #     y_label = 'Plot for ' + str(cols_plot[cnt])
                #     ax.set_ylabel(y_label)
                #     ax.set_ylim(-1.2, 1.2)
                #     cnt += 1
                # plt.show()
        else:
            return None

#ft = FilterTweets()
#crypto_tweets = ft.filter_tweets_by_wrds(key_crypto_words,tweets)
#token_tweets = ft.filter_tweets_by_wrds(key_token_words,tweets)

#ft.get_sentiments(token_tweets)



