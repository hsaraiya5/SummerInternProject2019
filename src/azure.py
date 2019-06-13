import requests
import pandas as pd
# pprint is used to format the JSON response
from pprint import pprint
import json
from IPython.display import HTML
import csv
from csv import DictWriter
import sys
import os
import simplejson



# -------------------- Set up Cognitive Services -------------------------------------------------#
subscription_key = "49912eb60afc4af1889999e11f5d51c1"
endpoint = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_url = endpoint + "sentiment"
keyPhrases_url = endpoint + "keyPhrases"
languages_url = endpoint + "languages"

headers   = {"Ocp-Apim-Subscription-Key": subscription_key}

#-------------------- Read the Data -------------------------------------------------------------#

### Crowd Tangle data
csv_file = "./data/CrowdTangle.csv"

ct_tweets = pd.read_csv(csv_file, sep = ",").rename({'Message':'text'}, axis='columns') #read in as pandas df
ct_tweets= ct_tweets.assign(id = ct_tweets.reset_index().index+1, language = ['en'] * ct_tweets.shape[0]) # add id and language column
tweets = pd.DataFrame(ct_tweets[['id','language','text']]) #.set_index('id')) #get just id, language, and text


tweets_dict = {"documents" : tweets.to_dict('records')} #convert df to dictionary



#-------------------- Language Detection -------------------------------------------------------#
response  = requests.post(languages_url, headers=headers, json=tweets_dict)
languages = response.json()
#pprint(languages)

#-------------------- Sentiment Analysis --------------------------------------------------------#

###  Use the Requests library to send the documents to the API
response  = requests.post(sentiment_url, headers=headers, json=tweets_dict)
sentiments = response.json()
#pprint(sentiments)

#--------------------- Keywords ----------------------------------------------------------------#
response = requests.post(keyPhrases_url, headers=headers, json=tweets_dict)
keyPhrases = response.json()
#pprint(keyPhrases)

sentimentValues = list(sentiments.values())

sentimentObjects = sentimentValues[0]

keyPhrasesValues = list(keyPhrases.values())

keyPhrasesObjects = keyPhrasesValues[0]


totalLength = len(sentimentValues[0])


df = pd.DataFrame(columns=['id', 'score', 'keyPhrases'])

for x in range(totalLength):
  df = df.append(pd.Series([sentimentObjects[x]['id'], sentimentObjects[x]['score'], keyPhrasesObjects[x]['keyPhrases']], index=df.columns), ignore_index=True)

export = pd.concat([ct_tweets.drop(['id','language'], axis=1),df.drop('id', axis=1)], axis=1)
export.to_csv('sentimentOutput2.csv')