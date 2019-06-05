import csv
import json
import pandas as pd
from pprint import pprint

#convert csv to json??


csv_file = pd.DataFrame(pd.read_csv("./data/CrowdTangle.csv", sep = ","))
print(csv_file.columns)

out = csv_file[['Message']].to_json(orient = 'records')
pprint(out)



# csv_file = open("./data/CrowdTangle.csv", 'r')
# json_file = open("./data/CrowdTangle.json", 'w')

# fieldnames = ('Account', 'User Name', 'Followers at Posting', 'Created', 'Type', 'Likes', 'Retweets', 'URL', 'text', 'Screen Name', 'Link 1', 'Final Link 1', 'Link 2', 'Final Link 2', 'Score')

# reader = csv.DictReader(csv_file,fieldnames=fieldnames)
# for row in reader:
#     json.dump(row, json_file)
#     jsonfile.write('/n')






# data = {}
# with open(csv_file, encoding = 'Latin-1') as csvFile:
#     csvReader = csv.DictReader(csvFile)
#     print(type(csvReader))
#     print(csvReader)
#     for rows in csvReader:
#         id = rows["ID"]
#         data[id] = rows

# print(data)
# #with open(json_file, 'w') as jasonFile:
#     #jsonfile.write(json.dump(data, indent = 4))