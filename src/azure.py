import requests
import pandas as pd
# pprint is used to format the JSON response
from pprint import pprint
import json
from IPython.display import HTML
import csv
import sys
import os

## reference : https://www.johanahlen.info/en/2017/04/text-analytics-and-sentiment-analysis-with-microsoft-cognitive-services/

# -------------------- Set up Cognitive Services -------------------------------------------------#
subscription_key = "b672d4a126bb4092824e5a7e389fc698"
endpoint = "https://northcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_url = endpoint + "sentiment"
keyPhrases_url = endpoint + "keyPhrases"
languages_url = endpoint + "languages"

headers   = {"Ocp-Apim-Subscription-Key": subscription_key}

print(sentiment_url)
print(keyPhrases_url)
print(languages_url)

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

tweets = ct_tweets[['text']].to_json(orient = 'records')
#ct_dict = ct_tweets.to_dict('dict') #convert to type dict
#ct_jason = json.dumps(ct_dict, indent=4)


#-------------------- Language Detection -------------------------------------------------------#
response  = requests.post(languages_url, headers=headers, json=tweets)
languages = response.json()
pprint(languages)

#-------------------- Sentiment Analysis --------------------------------------------------------#

###  Use the Requests library to send the documents to the API
response  = requests.post(sentiment_url, headers=headers, json=documents)
sentiments = response.json()
pprint(sentiments)

#--------------------- Keywords ----------------------------------------------------------------#
response = requests.post(keyPhrases_url, headers=headers, json=documents)
keyPhrases = response.json()
pprint(keyPhrases)


