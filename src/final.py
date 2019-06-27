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
import numpy as np
import mysql.connector


# Setting up access key, secret key, and api in order to get tweets
auth = tweepy.auth.OAuthHandler('DSES0LTFK2vAFV3zGAwQlJXDa', 'KLVUqauEqqelnZZPry9GPTvHuLrY3nnk3FkV5kmGtdKsodkhbQ')
auth.set_access_token('1131180954851131392-3mM1DFFs1CRr80YaBMsMrMXSrw5hC9', 's9STIOmxPZHXyDo6I3GYUorJ29LDYa2SGpPru6Os9MGtc')
api = tweepy.API(auth)

# Set up Cognitive Services
subscription_key = "0927e8dd00424bad9a18ffef4c0a2618"
endpoint = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_url = endpoint + "sentiment"
keyPhrases_url = endpoint + "keyPhrases"
languages_url = endpoint + "languages"
headers   = {"Ocp-Apim-Subscription-Key": subscription_key}


  

categories_df = pd.read_csv('src/categories.csv')

print(categories_df)
categories_list = list(categories_df.columns.values)

print(categories_list)

category_name = input("Please enter the name of the category you would like to add/update: ")
if category_name not in categories_list:
  categories_df[category_name] = 'test'


phrase = input("Please enter the keyword/phrase you would like to add to the category: ")

keywords = list(categories_df[category_name])
print(keywords)
if phrase not in keywords:
  keywords.append(phrase)
  categories_df[category_name] = keywords
else:
  print("The phrase '" + phrase + "' already exists within this category")

categories_df.to_csv("src/categories.csv")








query = input("Enter a search term/phrase: ")
date = input("Enter data from which you want tweets (YYYY-MM-DD): ")

# Obtaining tweets based on search query, and specified number of tweets
queries = [query]


query = query.replace(" ", "")
csvFileName = 'finalData/' + query + '.csv'
for i in range(len(queries)):
  search_results = api.search(q = queries[i], until= date)
  # Opening new CSV file and writing tweet info to file
  
  csvFile = open(csvFileName, 'a')
  csvWriter = csv.writer(csvFile)
  for tweet in search_results:
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'), tweet.favorite_count, tweet.retweet_count])
  csvFile.close()




#-Read in tweets from CSV to a dataframe
os.chdir('./finalData')
fileName = query +'.csv'
tweets = pd.read_csv(fileName, header = None)
tweets.columns = ['Time','Tweet', 'Favorites', 'Retweets']


# Clean the text of each tweet
def clean_tweet(string):
    #string = string.replace('\n','')
    return(re.sub(r"\\x\w\w","",string)[1:].strip('\'').strip('\"'))

tweets['Tweet'] = tweets['Tweet'].apply(clean_tweet)


# Re-format to run tweets through azure api
tweets= tweets.assign(id = tweets.reset_index().index+1, language = ['en'] * tweets.shape[0]).rename({'Tweet':'text'}, axis='columns') # add id and language column
tweets_temp = pd.DataFrame(tweets[['id','language','text']]) #.set_index('id')) #get just id, language, and text
tweets_dict = {"documents" : tweets_temp.to_dict('records')} #convert df to dictionary

# Language Detection
response  = requests.post(languages_url, headers=headers, json=tweets_dict)
languages = response.json()

# Sentiment Analysis
response  = requests.post(sentiment_url, headers=headers, json=tweets_dict)
sentiments = response.json()
#pprint(sentiments)

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

# combine azure data to original data
export = pd.concat([tweets.drop(['id','language'], axis=1).rename({'text':'Tweet'}, axis='columns'),df.drop('id', axis=1).rename({'score':'Sentiment'}, axis='columns')], axis=1)
csvFileName = query + 'final.csv'
export.to_csv(csvFileName)
os.remove(fileName)
