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

categories_new = []

##################################### ACCESS TWITTER AND AZURE API #########################################################
# Setting up access key, secret key, and api in order to get tweets
auth = tweepy.auth.OAuthHandler('DSES0LTFK2vAFV3zGAwQlJXDa', 'KLVUqauEqqelnZZPry9GPTvHuLrY3nnk3FkV5kmGtdKsodkhbQ')
auth.set_access_token('1131180954851131392-3mM1DFFs1CRr80YaBMsMrMXSrw5hC9', 's9STIOmxPZHXyDo6I3GYUorJ29LDYa2SGpPru6Os9MGtc')
api = tweepy.API(auth)

# Set up Cognitive Services
subscription_key = "823c2e253d274b019cf1eed017916825"
endpoint = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_url = endpoint + "sentiment"
keyPhrases_url = endpoint + "keyPhrases"
languages_url = endpoint + "languages"
headers   = {"Ocp-Apim-Subscription-Key": subscription_key}








####################################### USER INPUT FOR TWITTER QUERIES #########################################################
categories_df = pd.read_csv('src/categories.csv')

#initialize lists
categories_list = list(categories_df.columns.values)
category = []
material = []
categories = pd.DataFrame({'Category': categories_list})

#----------------------------------- updating keywords database ----------------------------------------------------------------
userInput = input("Would you like to update the keywords database? (Y/N): ")
if userInput == 'Y':

  userAnswer = 'Y'
  while userAnswer == 'Y':
    
    categories_df = pd.read_csv('src/categories.csv')

    print(categories_df)


    category_name = input("Please enter the name of the category you would like to add/update: ")
    if category_name not in categories_list:
      categories_df[category_name] = 'o'


    phrase = input("Please enter the keyword/phrase you would like to add to the category: ")

    keywords = list(categories_df[category_name])
    index = keywords.index('o')
    if phrase not in keywords:
      keywords[index] = phrase
      categories_df[category_name] = keywords
    else:
      print("The phrase '" + phrase + "' already exists within this category")

    userAnswer = input("Would you like to keep updating/adding to the set of key phrases? (Y/N): ")
    categories_df.to_csv('src/categories.csv', index=False)
    
    # content Catgories
    categories_new = list(categories_df.columns.values)
    categories = pd.DataFrame({'Category': categories_new})

#---------------------------------ask user for Categories | Keywords -------------------------------------------------

### Decide which category/keywords/materials to search for
searchAnswer = input("Would you like to run a search? (Y/N): ")

#c = 'o'
if searchAnswer == 'Y': 
  
  #### USER SELECTS MATERIALS ###
  print("""

  """)
  userInput = input("""Which materials would you like to search for (glass/plastic/aluminum can)?

  If selecting multiple, separate by comma. ex: glass, plastic
  If you would like to search for all keywords type ALL
    
Enter: """)
  if userInput == 'ALL':
    material = ['glass','plastic','aluminum can']
  else:
    for i in userInput.split(","):
      material.append(i.strip())

  
  ### choose category/categories to query for
  categoryChoices = list(categories_df.columns.values)
  print(categoryChoices)

  userInput = input("""Please indicate which categories you would like to search for.

  If selecting multiple, separate by comma. ex: Cost, Sustainability, Innovation.
  If you would like to select all categories type ALL
  
Enter: """)
  print(userInput)

###### QUERY FOR ALL POSSIBLE CATEGORIES | KEYWORDS ######### 
  if userInput == 'ALL':
    category = categoryChoices
    for c in category:
      keyword = list(categories_df[category[c]])
      testIndex = keyword.index('o')
      keyword = keyword[:testIndex]

      ## Get the Tweets
      csvFileName = 'finalData/' + c + '.csv'
  
      for m in material:
        for k in keyword:
          query = m + ' ' + k
          search_results = api.search(q = query, lang = 'en',tweet_mode = "extended", count=500)
          # Opening new CSV file and writing tweet info to file
          print("Obtain Tweets for query: " + query)
          csvFile = open(csvFileName, 'a')
          csvWriter = csv.writer(csvFile)
          for tweet in search_results:
            csvWriter.writerow([tweet.created_at, tweet.full_text.encode('utf-8'), tweet.favorite_count, tweet.retweet_count, m])
          csvFile.close()      
  
  ###### QUERY FOR SELECT CATEGORIES | KEYWORDS ######### 
  else:
    for i in userInput.split(","):
      category.append(i.strip())
    for c in category:
      keyword_search = []
      keyword = list(categories_df[c])
      testIndex = keyword.index('o')
      keyword = keyword[:testIndex]
      print("""

""")
      print("For category: " + c)
      print(keyword) ### choose keywords to search for 
      userInput = input("""Which keywords would you like to search for?

  If selecting multiple, separate by comma. ex: keyword1, keyword2
  If you would like to search for all keywords type ALL
    
Enter: """)
      if userInput == "ALL":
        keyword_search = keyword
      else:
        for i in userInput.split(","):
          keyword_search.append(i.strip())

      ### Obtain the tweets
      csvFileName = 'finalData/' + c + '.csv'
      
      for m in material:
        for k in keyword_search:
          query = m + ' ' + k
          search_results = api.search(q = query, lang = 'en',tweet_mode = "extended", count=500)
          # Opening new CSV file and writing tweet info to file
          print("Obtain Tweets for query: " + query)
          csvFile = open(csvFileName, 'a')
          csvWriter = csv.writer(csvFile)
          for tweet in search_results:
            csvWriter.writerow([tweet.created_at, tweet.full_text.encode('utf-8'), tweet.favorite_count, tweet.retweet_count, m])
          csvFile.close()      












####################################### FORMAT TWEETS #########################################################

os.chdir('./finalData')
for c in category:
  #-Read in tweets from CSV to a dataframe
  fileName = c +'.csv'
  if(os.stat(fileName).st_size == 0):
    os.remove(fileName)
    sys.exit('No tweets pulled for ' + c + 'category')
  else:
    tweets = pd.read_csv(fileName, header = None)
  tweets.columns = ['Time','Tweet', 'Favorites', 'Retweets', 'Material']
  

  # Clean the text of each tweet
  def clean_tweet(string):
    return(re.sub(r"\\x\w\w","",string)[1:].strip('\'').strip('\"'))

  tweets['Tweet'] = tweets['Tweet'].apply(clean_tweet)


#  Re-format to run tweets through azure api
  tweets= tweets.assign(id = tweets.reset_index().index+1, language = ['en'] * tweets.shape[0]).rename({'Tweet':'text'}, axis='columns') # add id and language column
  tweets_temp = pd.DataFrame(tweets[['id','language','text']]) #.set_index('id')) #get just id, language, and text
  tweets_dict = {"documents" : tweets_temp.to_dict('records')} #convert df to dictionary









####################################### RUN AZURE TEXT ANALYTICS (SENTIMENT & KEYPHRASES) #########################################################
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
  print(totalLength)
  df = pd.DataFrame(columns=['id', 'score', 'keyPhrases'])
  print(range(totalLength))
  for x in range(totalLength):
    df = df.append(pd.Series([sentimentObjects[x]['id'], sentimentObjects[x]['score'], keyPhrasesObjects[x]['keyPhrases']], index=df.columns), ignore_index=True)

  os.remove(fileName)

####################################### FORMAT DATA FOR EXCEL EXPORT #########################################################
  # combine azure data to original data
  export = pd.concat([tweets.drop(['id', 'language'], axis=1).rename({'text':'Tweet'}, axis='columns'),df.drop('id', axis=1).rename({'score':'Sentiment'}, axis='columns')], axis=1)
  export = export.assign(Category1=c, Category2="", Category3="", Irrelevent = 0, News=0) 
  export = export[['Time','Tweet', 'Favorites', 'Retweets', 'Sentiment', 'Material','Category1', 'Category2', 'Category3', 'keyPhrases', 'News', 'Irrelevent']] #reorder columns

  #export csv
  csvFileName = c + 'final.csv'
  export.to_csv(csvFileName)
  os.remove(csvFileName)








####################################### EXPORT DATA TO EXCEL WORKBOOK #########################################################
  ## check if file exists
  xlFileName = './' + c + 'final.xlsx'

  import os.path
  from os import path
  print('Create and open excel workbook for ' + c)
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
    if len(categories_new) > len(categories_list):
      categories.to_excel(writer, "Sheet 2") 

    writer.save()
  else:
    print(xlFileName+' new')
    write = pd.ExcelWriter(xlFileName, engine='xlsxwriter')
    export.to_excel(write, sheet_name='Sheet 1', index=False)
    categories.to_excel(write, sheet_name='Sheet 2')
    write.save()
