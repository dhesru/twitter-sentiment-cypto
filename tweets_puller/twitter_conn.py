import os
import tweepy
import json

cwd = os.getcwd()
json_file_path = cwd + "/" + "creds.json"

with open(json_file_path) as json_file:
    json_data = json.load(json_file)

access_token = json_data.get('access_token')
access_token_secret = json_data.get('access_token_secret')
consumer_key = json_data.get('consumer_key')
consumer_secret = json_data.get('consumer_secret')




class TwitterConn():
    access_token = json_data.get('access_token')
    access_token_secret = json_data.get('access_token_secret')
    consumer_key = json_data.get('consumer_key')
    consumer_secret = json_data.get('consumer_secret')

    def conn(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        api = tweepy.API(auth)
        return api
