# Importing dependencies
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from config import password
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, normalize
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

## ------------------------------ Functions------------------------------- ##
def top_10_feature(x, y):
    df = pd.DataFrame.from_dict(x, orient='index')

    sorted_df = df.sort_values(by=y, ascending=False).head(10).reset_index()

    top_titles = sorted_df['index'].to_list()
    filtered_list = sorted_df[y].to_list()

    return top_titles, filtered_list

# Defining a function to check if there are any non-dict elements in a list
def checkType(a_list):
    types = [0, 0, 0]
    indexes = []
    for element in a_list:
        if isinstance(element, dict):
            types[0] += 1
        else:
            types[1] += 1
            indexes.append(a_list.index(element))
            types[2] = indexes
    return types

# Defining a function for the euclidean distance between two points
def distance(x1, x2):
    d = np.sqrt(pow((x2[1] - x1[1]), 2) - pow((x2[0] - x1[0]), 2))
    return d

# Defining a function that calculates the average co-ordinates
def averagePoint(arr):
    x = 0
    y = 0
    count = 0
    for i in arr:
        x += i[0]
        y += i[1]
        count += 1
    
    x = x / count
    y = y / count
    
    return [x, y]

# Defining a function to convert strings to Json objects / dictionaries
def stringtoJson(a):
    result = None
    
    try:
        if len(a) > 3:
            result = json.loads(a.replace("'", "\""))
        else:
            result = " "
    except:
        result = " "
    
    return result

def findRating(arr):
    max_rating = 0
    best_title = ""

    for i in arr:
        if (list(r.loc[r['title'] == str(i)]['rating'])[0]) > max_rating:
            max_rating = list(r.loc[r['title'] == str(i)]['rating'])[0]
            best_title = list(r.loc[r['title'] == str(i)]['title'])[0]

    return best_title

def findPCA(string):
    a = d['title'].loc[d['title'] == string].index[0]
    b = list(pca_df.iloc[a, :].values)

    return b
## --------------------------------------------------------------------- ##

## ------------------------------ Classes ------------------------------- ##
class steamPredictor:
    """
    requirements:
    - averagePoint & distance functions
    - pca_df which includes two dimension
    - y which is a pandas series of game titles
    - r which is a df containing the rating of each game
    """
    def __init__(self):
        self = self
    
    def prediction(self, inputs):  
        a, b, c = inputs # strings
        
        a = findPCA(a) 
        b = findPCA(b) # PCA values
        c = findPCA(c) 
        
        games = [a, b, c]
        results = []
        
        for game in games:
            minimum = 1000
            tracker = 1
            for i in range(0, len(d)):
                x2 = pca_df.iloc[i, :2]
                a = distance(game, x2)
                if a > 0 and a < minimum:
                    minimum = a
                    tracker = i
            if y['title'][tracker] not in inputs:
                results.append(y['title'][tracker])
        
        best_fit = findRating(results)
        
        return best_fit
## --------------------------------------------------------------------- ##

## ------------------------------ Part 1------------------------------- ##
# Initialising the app and starting the connection to the data source
app = Flask(__name__)

conn = f"mongodb+srv://admin:{password}@cluster0.tflk7.mongodb.net/games_info_db?retryWrites=true&w=majority"
mongo = PyMongo(app, uri = conn)

collection = mongo.db.game_info
game_data = collection.find_one()

del game_data['_id']

game_df = pd.DataFrame.from_dict(game_data, orient='index').reset_index()

print(game_data['Dota 2'])
print(type(game_data))
## --------------------------------------------------------------------- ##

## ------------------------------ Part 2------------------------------- ##
# Reading the data source
df = pd.read_csv('resources/game_data.csv')

# Creating a new column of dictionaries
df['dictionaries'] = df['tags'].apply(lambda x: stringtoJson(x))

tags = df.loc[df['dictionaries'] != " "]['dictionaries'].to_list()
missed = df.loc[df['dictionaries'] == " "].index.to_list()

# Creating a dataframe from the dictionaries
d = pd.DataFrame(tags)

# Creating a pandas series of game titles
y = df['name']

# Creating a list of game titles
names = list(y)

# Removing the elements which had missing tag information
for index in sorted(missed, reverse=True):
    del names[index]
    
# Adding a new column to the df
d['title'] = names

d.fillna(0, inplace=True)

# Finding the summary statistics of the data
info_df = d.describe()

# Removing the features which received no more than 7500 votes for any particular game
to_drop = [c for c in info_df.columns if info_df[c]['max'] < 7500]

# Removing the unwanted features
d.drop(to_drop, axis=1, inplace=True)

# Creating a test df containing only numeric features
test_df = d.drop('title', axis=1)

# Adding a sum of each row column
test_df['sum'] = test_df.iloc[:, :-1].sum(axis=1)

# Finding any games with no values remaining (due to feature selection)
to_drop = []

for index, row in test_df.loc[test_df['sum'] == 0].iterrows():
    to_drop.append(index)
    
d.drop(d.index[to_drop], inplace=True)

# Defining the X and y variables for the model
X = d.drop('title', axis=1)
y = d[['title']]

# Creating a standard scaler and transforming the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled.shape

# Performing PCA on the features
pca = PCA(n_components = 2)
principal_comp = pca.fit_transform(X_scaled)

# Creating a dataframe with the PCA data
pca_df = pd.DataFrame(data = principal_comp, columns = ["pca1", "pca2"])

r = df[['name', 'positive', 'negative']]

r.columns = ['title', 'positive', 'negative']
r['rating'] = r['positive'] / (r['positive'] + r['negative'])

model = steamPredictor()
## --------------------------------------------------------------------- ##

## ------------------------------ Routes ------------------------------- ##
@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/graphs")
def graphs():
    
    return render_template("graphs.html")

@app.route("/predictor")
def predictor():
    
    return render_template("predictor.html")

@app.route("/data")
def data():
    top_games, concurrent_players = top_10_feature(game_data, 'ccu')

    top_discount, highest_discount = top_10_feature(game_data, 'discount')

    return jsonify(game_data, top_games, concurrent_players, top_discount, highest_discount)

@app.route("/players")
def players():
    games1, avg_2weeks = top_10_feature(game_data, 'average_2weeks')
    games2, med_2weeks = top_10_feature(game_data, 'median_2weeks')

    return jsonify(games1, avg_2weeks, games2, med_2weeks)

@app.route("/reviews")
def reviews():
    rating_df = game_df[['index', 'positive', 'negative']]
    rating_df['rating'] = rating_df['positive'] / (rating_df['positive'] + rating_df['negative'])

    a = rating_df.sort_values(by='rating', ascending=False).head(10)['index'].tolist()
    b = rating_df.sort_values(by='rating', ascending=False).head(10)['rating'].tolist()

    return jsonify(a, b)

@app.route("/devs")
def devs():
    a = game_df.groupby('developer').count().sort_values(by='appid', ascending=False).head(10)['index'].index.tolist()
    b = [i for i in game_df.groupby('developer').count().sort_values(by='appid', ascending=False).head(10)['index']]

    return jsonify(a, b)

@app.route("/prediction/<arr>")
def prediction(arr):

    a = arr.split(",")

    result = model.prediction(a)
    
    return jsonify(result)
## --------------------------------------------------------------------- ##

if __name__ == "__main__":
    app.run(debug=True)