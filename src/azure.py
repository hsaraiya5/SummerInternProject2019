import requests
import pandas as pd
# pprint is used to format the JSON response
from pprint import pprint
import json
from IPython.display import HTML
import csv
import sys
import os


# -------------------- Set up Cognitive Services -------------------------------------------------#
subscription_key = "b672d4a126bb4092824e5a7e389fc698"
endpoint = "https://northcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_url = endpoint + "sentiment"
keyPhrases_url = endpoint + "keyPhrases"
languages_url = endpoint + "languages"

headers   = {"Ocp-Apim-Subscription-Key": subscription_key}

#-------------------- Read the Data -------------------------------------------------------------#
### Azure text example
### Documents dictionary with ID, and Text tuples.
documents = {"documents" : [
  {"id": "1", "language": "en", "text": "I had a wonderful experience! The rooms were wonderful and the staff was helpful."},
  {"id": "2", "language": "en", "text": "I had a terrible time at the hotel. The staff was rude and the food was awful."},  
  {"id": "3", "language": "es", "text": "Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos."},  
  {"id": "4", "language": "es", "text": "La carretera estaba atascada. Había mucho tráfico el día de ayer."}
]}

### Crowd Tangle data
csv_file = "./data/CrowdTangle.csv"

ct_tweets = pd.read_csv(csv_file, sep = ",").rename({'Message':'text'}, axis='columns') #read in as pandas df
ct_tweets= ct_tweets.assign(id = ct_tweets.reset_index().index+1, language = ['en'] * ct_tweets.shape[0]) # add id and language column
tweets = pd.DataFrame(ct_tweets[['id','language','text']]) #.set_index('id')) #get just id, language, and text


tweets_dict = {"documents" : tweets.to_dict('records')} #convert df to dictionary



#-------------------- Language Detection -------------------------------------------------------#
response  = requests.post(languages_url, headers=headers, json=tweets_dict)
languages = response.json()
pprint(languages)

#-------------------- Sentiment Analysis --------------------------------------------------------#

###  Use the Requests library to send the documents to the API
response  = requests.post(sentiment_url, headers=headers, json=tweets_dict)
sentiments = response.json()
pprint(sentiments)

#--------------------- Keywords ----------------------------------------------------------------#
response = requests.post(keyPhrases_url, headers=headers, json=tweets_dict)
keyPhrases = response.json()
pprint(keyPhrases)


