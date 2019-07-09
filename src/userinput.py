import pandas as pd
import os

categories_df = pd.read_csv('src/categories.csv')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
  else:
    for i in userInput.split(","):
      category.append(i.strip())
    for c in category:
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
      for i in userInput.split(","):
        keyword_search.append(i.strip())

#check for materials.
print("""

""")
userInput = input("""Which materials would you like to search for (glass/plastic/aluminum can)?

  If selecting multiple, separate by comma. ex: glass, plastic
  If you would like to search for all keywords type ALL
    
Enter: """)
if userInput == 'ALL':
  material = ['glass','plastic', 'aluminum can']
else:
    for i in userInput.split(","):
      material.append(i.strip())

### process each query

# cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
for c in category:
 print('Create and open excel workbook for ' + c)
 # mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
 for m in material:
    for k in keyword_search:
      query = m + ' ' + k
      # kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
      print("Obtain Tweets and export to " +  c + " workbook for the query: " + query) #lines 84-97


# print("Read Tweets csv and make dataframe for the azure api")


