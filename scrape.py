# Import dependencies
import json
import requests
import time
import pandas as pd
import pymongo
from config import password

# Creating an empty dictionary to hold API responses
game_data = {}

# Building the query URLs
url = 'https://steamspy.com/api.php?request=all&page='
query_url = [url + str(x) for x in range(0, 1)]

# Calling the API
for url in query_url:    
    try:
        response = requests.get(url)
        time.sleep(1)
        
        # Updating the dictionary with the response
        game_data.update(response.json())
    except:
        print('Get request failed')

# Creating a list from the App IDs
app_ids = [i for i in game_data]

missed = []
full_data = {}

url = 'https://steamspy.com/api.php?request=appdetails&appid='

t0 = time.time()
for i in range(0, len(app_ids)):
    try:
        response = requests.get(url + str(app_ids[i]))
        full_data[app_ids[i]] = response.json()
    except:
        missed.append(app_ids[i])

t1 = time.time()
print(f'{len(full_data)}, {t1-t0}')

# Cleaning the data
game_df = pd.DataFrame.from_dict(full_data, orient='index')
game_df.reset_index(drop=True, inplace=True)

game_df.drop(['score_rank', 'userscore', 'languages'], inplace=True, axis=1)
game_df[['price', 'initialprice', 'discount']] = game_df[['price', 'initialprice', 'discount']].apply(pd.to_numeric)

# Checking the results
print(f'Number of games: {len(game_df)}')
print(f'\n{game_df.columns}\n')

# Setting the index to the name of the game
game_df.set_index('name', inplace=True)

# Creating a dictionary
game_df.to_csv('resources/game_data.csv')
d = game_df.T.to_dict()

# Creating a connection to the MongoDB database
conn = f"mongodb+srv://admin:{password}@cluster0.tflk7.mongodb.net/games_info_db?retryWrites=true&w=majority"
client = pymongo.MongoClient(conn)

# Connecting to the correct database and collection
db = client.games_info_db
game_info = db.game_info

# Updating the data in the collection with the scrape results
game_info.update({}, d, upsert = True)

# Closing the connection
client.close()