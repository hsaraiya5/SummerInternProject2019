import pandas as pd
import tweepy
import csv

auth = tweepy.auth.OAuthHandler('DSES0LTFK2vAFV3zGAwQlJXDa', 'KLVUqauEqqelnZZPry9GPTvHuLrY3nnk3FkV5kmGtdKsodkhbQ')
auth.set_access_token('1131180954851131392-3mM1DFFs1CRr80YaBMsMrMXSrw5hC9', 's9STIOmxPZHXyDo6I3GYUorJ29LDYa2SGpPru6Os9MGtc')

api = tweepy.API(auth)

csvFile = open('data/newTweets.csv', 'a')
csvWriter = csv.writer(csvFile)

search_results = api.search(q ="glass bottle",count = 100)


#for tweet in search_results:
#    tweet.text = tweet.text[2:]

for tweet in search_results:
    print(tweet.text)
    print('\n')
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'), tweet.favorite_count, tweet.retweet_count])


csvFile.close()
