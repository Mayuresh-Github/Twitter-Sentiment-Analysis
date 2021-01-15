# Imports

"""
    tweepy is used for handling the Twitter API.
    Authorization, fetching tweets and everything is done using tweepy
"""
import tweepy

from twitter_analyze import TwitterSentiment

from custom_input import CustomSentiment

# Authorization of Twitter API
auth = tweepy.OAuthHandler("IrTKOcdQzkDosVyKimjkwu4ha", "Zwfi6hkDGouh5xfwdj9naPVXO9M8fNvYggswPcLwPBmFMJpgv5")
auth.set_access_token("1258597505412894720-iyeAXocmtVB77YTiWnPND3irqLwHXT",
                      "IajZmQPjy6F17fVlhvmgIIb1AdAxoJ9lMeMNO6TQKE4Lz")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
try:
    api.verify_credentials()
    print("Authentication done!!")
except:
    print("\nError verifying credentials")

if api is not None:
    print("\n"
          "*************************************************************************"
          "\nSuccessful Verification!"
          "\nYou are ready to fetch tweets!!\n"
          "*************************************************************************\n")
    choiceToDo = int(input("1. Fetch and Analyze Tweets from Twitter"
                           "\n2. Custom input"
                           "\nEnter choice: "))
    if choiceToDo == 1:
        search_key = input("Enter search keyword for tweets: ")
        first = TwitterSentiment(api)
        TwitterSentiment.tweets_analyze(first, search_key=search_key)
    elif choiceToDo == 2:
        CustomSentiment.analyze()
    else:
        print("Enter correct choice")

else:
    print("\n"
          "*************************************************************************"
          "\nError while verification."
          "\nCheck credentials.\n"
          "*************************************************************************\n")
