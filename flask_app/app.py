# flask_web/app.py

from flask import Flask, render_template
import json
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
from tweets_puller.tweets_puller import FilterTweets
from tweets_puller.twitter_conn import TwitterConn

import plotly
import plotly.express as px

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/get_crypto_sentiments')
def get_crypto_sentimnets():
    twt_conn_api = TwitterConn().conn()

    key_crypto_words = ['address', 'altcoin', 'bitcoin', 'eth', 'sol', 'blockchain', 'btfd', 'dapps', 'defi', 'fiat',
                        'fork', 'gas', 'halving', 'hash rate', 'hodl',
                        'ico', 'mining', 'nft', 'pump and dump', 'satoshi', 'stablecoin', 'token', 'to the moon',
                        'rekt', 'wallet', 'whale', 'dip', 'crypto']

    key_token_words = ['ice', 'spell', 'time', 'solid']

    tweets = twt_conn_api.user_timeline(screen_name='danielesesta', count=5000, include_rts=False)


    ft_class = FilterTweets()
    filtered_tweet = ft_class.filter_tweets_by_wrds(filter_words=key_crypto_words,tweets=tweets)
    senti_data = ft_class.get_sentiments(filtered_tweet)

    tweets_df = pd.DataFrame.from_dict(senti_data)

    fig = px.line(tweets_df,y='pos',x='created_at')
    #fig.show()


    graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
