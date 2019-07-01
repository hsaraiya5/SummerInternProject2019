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

from openpyxl import load_workbook



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

userInput = input("Would you like to update the keywords database? (Y/N): ")
if userInput == 'Y':

  userAnswer = 'Y'
  while userAnswer == 'Y':
    
    categories_df = pd.read_csv('src/categories.csv')

    print(categories_df)
    categories_list = list(categories_df.columns.values)


    category_name = input("Please enter the name of the category you would like to add/update: ")
    if category_name not in categories_list:
      categories_df[category_name] = '0'


    phrase = input("Please enter the keyword/phrase you would like to add to the category: ")

    keywords = list(categories_df[category_name])
    index = keywords.index('0')
    if phrase not in keywords:
      keywords[index] = phrase
      categories_df[category_name] = keywords
    else:
      print("The phrase '" + phrase + "' already exists within this category")

    userAnswer = input("Would you like to keep updating/adding to the set of key phrases? (Y/N): ")
    categories_df.to_csv("src/categories.csv", index=False)


searchAnswer = input("Would you like to run a search? (Y/N): ")

searchCategory = '0'
if searchAnswer == 'Y':
  categoryChoices = list(categories_df.columns.values)
  print(categoryChoices)
  searchCategory = input("Please select a category name from the choices above: ")
  keywordChoices = list(categories_df[searchCategory])
  testIndex = keywordChoices.index('0')
  print(keywordChoices[:testIndex]
  keywordAnswer = input("Please select a keyword to search from the choices above: ")


material = input("What material would you like to search about? (glass/plastic/aluminum can): ")

query = material + keywordAnswer
date = input("Enter data from which you want tweets (YYYY-MM-DD): ")

# Obtaining tweets based on search query, and specified number of tweets
queries = [query]


query = query.replace(" ", "")
csvFileName = 'finalData/' + searchCategory + '.csv'
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
fileName = searchCategory +'.csv'
tweets = pd.read_csv(fileName, header = None)
tweets.columns = ['Time','Tweet', 'Favorites', 'Retweets']


# Clean the text of each tweet
def clean_tweet(string):
    return(re.sub(r"\\x\w\w","",string)[1:].strip('\'').strip('\"'))

tweets['Tweet'] = tweets['Tweet'].apply(clean_tweet)


# Re-format to run tweets through azure api
tweets= tweets.assign(id = tweets.reset_index().index+1, language = ['en'] * tweets.shape[0]).rename({'Tweet':'text'}, axis='columns') # add id and language column
tweets_temp = pd.DataFrame(tweets[['id','language','text']]) #.set_index('id')) #get just id, language, and text
tweets_dict = {"documents" : tweets_temp.to_dict('records')} #convert df to dictionary

# Language Detection
#response  = requests.post(languages_url, headers=headers, json=tweets_dict)
#languages = response.json()

# Sentiment Analysis
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

# combine azure data to original data
export = pd.concat([tweets.drop(['id', 'language'], axis=1).rename({'text':'Tweet'}, axis='columns'),df.drop('id', axis=1).rename({'score':'Sentiment'}, axis='columns')], axis=1)
# content Catgories
categories = pd.DataFrame({'Category': categories_df.columns.values})
export = export.assign(Material = material, Category1=searchCategory, Category2="", Category3="", Irrelevent = 0, News=0) 
export = export[['Time','Tweet', 'Favorites', 'Retweets', 'Sentiment', 'Material','Category1', 'Category2', 'Category3', 'keyPhrases', 'News', 'Irrelevent']] #reorder columns

#export csv
csvFileName = searchCategory + 'final.csv'
export.to_csv(csvFileName)
os.remove(fileName)
os.remove(csvFileName)

# export/append to excel workbook
## check if file exists
xlFileName = './' + searchCategory + 'final.xlsx'

import os.path
from os import path

if path.exists(xlFileName):
    print(xlFileName + ' exists') #Confirmation message
    temp = pd.read_excel(xlFileName) #Append new data to existing data
    export = temp.append(export)

    #export to excel workbook
    book = load_workbook(xlFileName)
    writer = pd.ExcelWriter(xlFileName, engine='openpyxl') 
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets) 

    export.to_excel(writer, "Sheet 1", index=False) 

    writer.save()
else:
    print(xlFileName+' new')
    write = pd.ExcelWriter(xlFileName, engine='xlsxwriter')
    export.to_excel(write, sheet_name='Sheet 1', index=False)
    categories.to_excel(write, sheet_name='Sheet 2')
    write.save()
