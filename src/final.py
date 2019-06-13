# Importing all necessary libraries used
import pandas as pd
import tweepy
import csv
import os
import re
import requests
from pprint import pprint
import json
from IPython.display import HTML
import csv
from csv import DictWriter
import sys
import simplejson


# Setting up access key, secret key, and api in order to get tweets
auth = tweepy.auth.OAuthHandler('DSES0LTFK2vAFV3zGAwQlJXDa', 'KLVUqauEqqelnZZPry9GPTvHuLrY3nnk3FkV5kmGtdKsodkhbQ')
auth.set_access_token('1131180954851131392-3mM1DFFs1CRr80YaBMsMrMXSrw5hC9', 's9STIOmxPZHXyDo6I3GYUorJ29LDYa2SGpPru6Os9MGtc')
api = tweepy.API(auth)

# Set up Cognitive Services
subscription_key = "49912eb60afc4af1889999e11f5d51c1"
endpoint = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_url = endpoint + "sentiment"
keyPhrases_url = endpoint + "keyPhrases"
languages_url = endpoint + "languages"
headers   = {"Ocp-Apim-Subscription-Key": subscription_key}


# Obtaining tweets based on search query, and specified number of tweets
search_results = api.search(q ="#sustainablelifestyle",count = 200)


# Opening new CSV file and writing tweet info to file
csvFile = open('data/sustainablelifestyle.csv', 'a')
csvWriter = csv.writer(csvFile)
for tweet in search_results:
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'), tweet.favorite_count, tweet.retweet_count])
csvFile.close()


#-Read in tweets from CSV to a dataframe
os.chdir('./data')
tweets = pd.read_csv("sustainablelifestyle.csv", header = None)
tweets.columns = ['Time','Tweet', 'Favorites', 'Retweets']


# Clean the text of each tweet
def clean_tweet(string):
    return(re.sub(r"\\x\w\w","",string)[1:].strip('\'').strip('\"'))

tweets['Tweet'] = tweets['Tweet'].apply(clean_tweet)


# Export tweets to new CSV file
#tweets.to_csv('sustainablelifestyleClean.csv', encoding='utf-8')


# Read in data to begin sentiment Analysis
#csv_file = "./data/sustainablelifestyleClean.csv"

#ct_tweets = pd.read_csv(csv_file, sep = ",").rename({'Tweet':'text'}, axis='columns') #read in as pandas df
tweets= tweets.assign(id = tweets.reset_index().index+1, language = ['en'] * tweets.shape[0]).rename({'Tweet':'text'}, axis='columns') # add id and language column
tweets_temp = pd.DataFrame(tweets[['id','language','text']]) #.set_index('id')) #get just id, language, and text
tweets_dict = {"documents" : tweets_temp.to_dict('records')} #convert df to dictionary

pprint(tweets_dict)
# Language Detection
response  = requests.post(languages_url, headers=headers, json=tweets_dict)
languages = response.json()

# Sentiment Analysis
###  Use the Requests library to send the documents to the API
response  = requests.post(sentiment_url, headers=headers, json=tweets_dict)
sentiments = response.json()

# Keywords
response = requests.post(keyPhrases_url, headers=headers, json=tweets_dict)
keyPhrases = response.json()


# Compiling all data about tweet and exporting as CSV
sentimentValues = list(sentiments.values())
sentimentObjects = sentimentValues[0]

keyPhrasesValues = list(keyPhrases.values())
keyPhrasesObjects = keyPhrasesValues[0]

totalLength = len(sentimentValues[0])

df = pd.DataFrame(columns=['id', 'score', 'keyPhrases'])

for x in range(totalLength):
  df = df.append(pd.Series([sentimentObjects[x]['id'], sentimentObjects[x]['score'], keyPhrasesObjects[x]['keyPhrases']], index=df.columns), ignore_index=True)

export = pd.concat([tweets.drop(['id','language'], axis=1).rename({'text':'Tweet'}, axis='columns'),df.drop('id', axis=1).rename({'score':'Sentiment'}, axis='columns')], axis=1)
export.to_csv('sustainablelifestyleOutput.csv')