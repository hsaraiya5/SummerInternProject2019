import pandas as pd 
from twython import Twython



python_tweets = Twython('NuPHGrUI05z0XWmFzrPdtaTyD', 'WD5mMXRtPB6WuqKJgVUoQ6H84RSy2vVxBUOMMCPcSFMZG4ikOQ')


query = {'q': 'glass bottle', 'result_type': 'popular', 'count': 10, 'lang': 'en'}


tweet_info = {'user': [], 'date': [], 'text': [], 'favorite_count': []} 
for status in python_tweets.search(**query)['statuses']:
    tweet_info['user'].append(status['user']['screen_name'])
    tweet_info['date'].append(status['created_at'])
    tweet_info['text'].append(status['text'])
    tweet_info['favorite_count'].append(status['favorite_count'])


df = pd.DataFrame(tweet_info)
df.sort_values(by = 'favorite_count', inplace = True, ascending = False)
df.head(5)

print(df)
