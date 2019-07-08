import pandas as pd
import os

categories_df = pd.read_csv('src/categories.csv')
keyword_search = []
category = []
material =[]
### check for updating keywords database
userInput = input("Would you like to update the keywords database? (Y/N): ")
if userInput == 'Y':

  userAnswer = 'Y'
  while userAnswer == 'Y':
    
    categories_df = pd.read_csv('src/categories.csv')

    print(categories_df)
    categories_list = list(categories_df.columns.values)


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

### Decide which category/keywords/materials to search for
searchAnswer = input("Would you like to run a search? (Y/N): ")

searchCategory = 'o'
if searchAnswer == 'Y': ### choose category/categories to query for
  categoryChoices = list(categories_df.columns.values)
  print(categoryChoices)

  userInput = input("""Please indicate which categories you would like to search for.

  If selecting multiple, separate by comma. ex: Cost, Sustainability, Innovation.
  If you would like to select all categories type ALL
  
Enter: """)
  print(userInput)

  if userInput == 'ALL':
    category = categoryChoices
    print(category)
    print('query for all Categories their respective keywords')
    for c in range(1,len(category)):
      keyword = list(categories_df[category[c]])
      testIndex = keyword.index('o')
      keyword = keyword[:testIndex]
      keyword_search = keyword_search + keyword
      #print(category[c] + ":  " + keyword)
  else:
    for i in userInput.split(","):
      category.append(i.strip())
    for c in category:
      print(c)
      keyword = list(categories_df[c])
      testIndex = keyword.index('o')
      keyword = keyword[:testIndex]
      print(keyword) ### choose keywords to search for 
      userInput = input("""Which keywords would you like to search for?

  If selecting multiple, separate by comma. ex: keyword1, keyword2
  If you would like to search for all keywords type ALL
    
Enter: """)
      for i in userInput.split(","):
        keyword_search.append(i.strip())

#check for materials.
userInput = input("""Which materials would you like to search for (glass/plastic/aluminum can)?

  If selecting multiple, separate by comma. ex: glass, plastic
  If you would like to search for all keywords type ALL
    
Enter: """)
if userInput == 'ALL':
  material = ['glass','plastic', 'aluminum can']
else:
    for i in userInput.split(","):
      material.append(i.strip())

print(category)
print(keyword_search)
print(material)

### process each query
for c in category:
 print('Create and open excel workbook for ' + c)
 for m in material:
    print(m)
    for k in keyword_search:
      query = m + ' ' + k
      print("Obtain Tweets and export to " +  c + " workbook for the query: " + query) #lines 84-97


# print("Read Tweets csv and make dataframe for the azure api")

















  # userInput = input("Would you like to search for all categories? (Y/N): ")
  # if userInput == 'N' :
  #   searchCategory = input("Please select a category name from the choices above: ")
  #   keywordChoices = list(categories_df[searchCategory])
  #   testIndex = keywordChoices.index('o')
  #   keyword = keywordChoices[:testIndex]
  #   print(keyword)

  #   userInput = input("Would you like to query all keywords? (Y/N): ")
  #   if userInput == 'N':
  #     keyword = input("Please select a keyword to search from the choices above: ")
  #   else:
  #     print('query for all keywords for category ' + searchCategory)
  # else:
  #   category = categoryChoices
  #   print('query for all Categories their respective keywords')
  #   for c in range(1,len(category)):
  #     keyword = list(categories_df[category[c]])
  #     testIndex = keyword.index('o')
  #     print(keyword)
    



















#searchCategory = 'Convenience'
#fileName = 'Testing123/srz/' + searchCategory +'.csv'
#if(os.stat(fileName).st_size == 0):
  #print('No tweets pulled for ' + searchCategory)
#else:
  #tweets = pd.read_csv(fileName, header = None)
#tweets = pd.read_csv(fileName, header = None)




















# categories_df = pd.read_csv('srz/categoriez.csv')

# userInput = input("Would you like to update the keywords database? (Y/N): ")
# if userInput == 'Y':

#   userAnswer = 'Y'
#   while userAnswer == 'Y':
    
#     categories_df = pd.read_csv('srz/categoriez.csv')

#     print(categories_df)
#     categories_list = list(categories_df.columns.values)


#     category_name = input("Please enter the name of the category you would like to add/update: ")
#     if category_name not in categories_list:
#       categories_df[category_name] = 'o'


#     phrase = input("Please enter the keyword/phrase you would like to add to the category: ")

#     keywords = list(categories_df[category_name])
#     index = keywords.index('o')
#     if phrase not in keywords:
#       keywords[index] = phrase
#       categories_df[category_name] = keywords
#     else:
#       print("The phrase '" + phrase + "' already exists within this category")

#     userAnswer = input("Would you like to keep updating/adding to the set of key phrases? (Y/N): ")
#     categories_df.to_csv("srz/categoriez.csv", index=False)


# searchAnswer = input("Would you like to run a search? (Y/N): ")

# searchCategory = 'o'
# if searchAnswer == 'Y':
#   categoryChoices = list(categories_df.columns.values)
#   print(categoryChoices)
#   searchCategory = input("Please select a category name from the choices above: ")
#   keywordChoices = list(categories_df[searchCategory])
#   testIndex = keywordChoices.index('o')
#   print(keywordChoices[:testIndex])
#   keywordAnswer = input("Please select a keyword to search from the choices above: ")


# material = input("What material would you like to search about? (glass/plastic/aluminum can): ")

# query = material + keywordAnswer
# #date = input("Enter data from which you want tweets (YYYY-MM-DD): ")

# # Obtaining tweets based on search query, and specified number of tweets
# queries = [query]


# query = query.replace(" ", "")


# #-Read in tweets from CSV to a dataframe
# #os.chdir('./finalData')
# fileName = searchCategory +'.csv'
# tweets = pd.read_csv(fileName, header = None)
# tweets.columns = ['Time','Tweet', 'Favorites', 'Retweets']
# os.remove(fileName)