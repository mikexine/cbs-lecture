#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
import config
import json
import arrow 

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_secret = config.access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth)

# print("TweetId,UserName,Timestamp,Url")

def process_tweet(doc):
    tweet_id = doc.get("id_str")
    user_id = doc.get("user").get("id_str")
    user_name = doc.get("user").get("screen_name")
    url = "https://twitter.com/%s/status/%s" % (user_id, tweet_id)
    timestamp = arrow.get(doc.get('created_at'), "ddd MMM DD HH:mm:ss Z YYYY").format('YYYY-MM-DD HH:mm:ss ZZ')
    # print("Tweet %s | User: %s | Link: %s" % (tweet_id, user_name, url))
    print("%s,%s,%s,%s" % (tweet_id, user_name, url,timestamp))



class MyListener(StreamListener):

    def on_data(self, data):
        doc = json.loads(data)
        if doc.get("limit") is None:
            process_tweet(doc)

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=["donald", "trump"])
