import pandas as pd
import os
import csv
import re


#------------- Manipulating before export?-------------------
#import tweepy
#from test2 import search_results

#-------------------- Read in tweets.csv --------------------------
os.chdir('./data')
tweets = pd.read_csv("tweets.csv", header = None)
tweets.columns = ['Time','Tweet']



#------------------- Clean ALL tweets -----------------------------
def clean_tweet(string):
    return(re.sub(r"\\x\w\w","",string)[1:].strip('\'').strip('\"'))

tweets['Tweet'] = tweets['Tweet'].apply(clean_tweet)

print(tweets.head)

#------------------- Export Tweets to CSV file --------------------
tweets.to_csv('cleanedtweets.csv', encoding='utf-8')


