import pandas as pd
import tweepy
import csv
import os
import re

auth = tweepy.auth.OAuthHandler('DSES0LTFK2vAFV3zGAwQlJXDa', 'KLVUqauEqqelnZZPry9GPTvHuLrY3nnk3FkV5kmGtdKsodkhbQ')
auth.set_access_token('1131180954851131392-3mM1DFFs1CRr80YaBMsMrMXSrw5hC9', 's9STIOmxPZHXyDo6I3GYUorJ29LDYa2SGpPru6Os9MGtc')

api = tweepy.API(auth)

csvFile = open('data/sustainablelifestyle.csv', 'a')
csvWriter = csv.writer(csvFile)

search_results = api.search(q ="#sustainablelifestyle",count = 200)


#for tweet in search_results:
#    tweet.text = tweet.text[2:]

for tweet in search_results:
    print(tweet.text)
    print('\n')
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'), tweet.favorite_count, tweet.retweet_count])




csvFile.close()
#-------------------- Read in tweets.csv --------------------------
os.chdir('./data')
tweets = pd.read_csv("sustainablelifestyle.csv", header = None)
tweets.columns = ['Time','Tweet', 'Favorites', 'Retweets']



#------------------- Clean ALL tweets -----------------------------
def clean_tweet(string):
    return(re.sub(r"\\x\w\w","",string)[1:].strip('\'').strip('\"'))

tweets['Tweet'] = tweets['Tweet'].apply(clean_tweet)

#------------------- Export Tweets to CSV file --------------------
tweets.to_csv('sustainablelifestyleClean.csv', encoding='utf-8')