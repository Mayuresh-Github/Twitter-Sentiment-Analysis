"""
    tweepy is used for handling the Twitter API.
    Authorization, fetching tweets and everything is done using tweepy
"""
from __future__ import unicode_literals

import csv
import pandas as pd
import matplotlib.pyplot as plt
import re

import tweepy
from textblob import TextBlob


class TwitterSentiment:
    positive_tweets = []
    positive_polarity = []
    positive_subjective = []

    negative_tweets = []
    negative_polarity = []
    negative_subjective = []

    neutral_tweets = []
    neutral_polarity = []
    neutral_subjective = []

    def __init__(self, api):
        self.api = api

    @classmethod
    def remove_url(cls, txt):
        return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

    def search_keyword(self, search_key):
        tweets = self.api.search(q=search_key, count=100)
        return tweets

    def tweets_analyze(self, search_key):

        tweets = self.search_keyword(search_key=search_key)

        # Remove URLs
        tweets_no_urls = [self.remove_url(tweet.text) for tweet in tweets]

        # Create textblob objects of the tweets
        sentiment_objects = [TextBlob(tweet) for tweet in tweets_no_urls]

        sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]

        sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])

        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot histogram of the polarity values
        sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25, 0.25, 0.5, 0.75, 1],
                          ax=ax,
                          color="purple")

        plt.title("Sentiments from Tweets"
                  "\n\nNegative ------------------------------- Neutral -------------------------------- Positive")
        plt.show()

        for tweet in sentiment_objects:
            if tweet.sentiment.polarity > 0:
                self.positive_tweets.append(tweet.string)
                self.positive_polarity.append(tweet.sentiment.polarity)
                self.positive_subjective.append(tweet.sentiment[1])

            elif tweet.sentiment.polarity < 0:
                self.negative_tweets.append(tweet.string)
                self.negative_polarity.append(tweet.sentiment.polarity)
                self.negative_subjective.append(tweet.sentiment[1])

            elif tweet.sentiment.polarity == 0:
                self.neutral_tweets.append(tweet.string)
                self.neutral_polarity.append(tweet.sentiment.polarity)
                self.neutral_subjective.append(tweet.sentiment[1])

        choice = input("\nDo you want to save results to a file? (y/N): ")
        if choice == "y" or choice == "Y" or choice == "Yes" or choice == "yes":
            field = ["Sentence", "Result", "Polarity", "Subjective"]
            rows = []

            for i in range(0, len(self.positive_tweets)):
                rows.append(
                    [self.positive_tweets[i], "Positive", self.positive_polarity[i], self.positive_subjective[i]])

            for j in range(0, len(self.negative_tweets)):
                rows.append(
                    [self.negative_tweets[j], "Negative", self.negative_polarity[j], self.negative_subjective[j]])

            for k in range(0, len(self.neutral_tweets)):
                rows.append(
                    [self.neutral_tweets[k], "Neutral", self.neutral_polarity[k], self.neutral_subjective[k]])

            try:
                with open('results_sentiment.csv', 'w') as f:
                    write = csv.writer(f)

                    write.writerow(field)
                    write.writerows(rows)
                    print("Saved results_sentiment.csv successfully!")
            except:
                print("Error Saving file")

        print("************************************************************")
