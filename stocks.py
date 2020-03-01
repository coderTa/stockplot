# imports all the needed libraries
from bs4 import BeautifulSoup as bs
import requests as r
from datetime import datetime
from pymongo import MongoClient
import time

c = MongoClient("mongodb://techster_ben:Iltcvm50!@techsterben-cluster-shard-00-00-zx79j.gcp.mongodb.net:27017,techsterben-cluster-shard-00-01-zx79j.gcp.mongodb.net:27017,techsterben-cluster-shard-00-02-zx79j.gcp.mongodb.net:27017/test?ssl=true&replicaSet=TechsterBen-Cluster-shard-0&authSource=admin&retryWrites=true")
database = c.Stocks
collection = database.Popular_stocks

cursor = collection.find({})
for document in cursor:
    print(document)

# This section of code manually adds a document to MongoDB
# collection.insert_one({'points': 34, 'rebounds': 13, 'min': 38, 'date': datetime(2018, 12, 17)})

# This gets the URL & values of the stocks
base_URL = "https://money.cnn.com/data/markets/"

while True:
    page = r.get(base_URL).text
    page = bs(page)
    companies = page.find_all("span", {"class": "stock-name"})
    prices = page.find_all("span", {"class": "stock-price"})

    stock_prices = {}

    for i in range(len(companies)):
        companies[i] = companies[i].text
        prices[i] = prices[i].text

        stock_prices[companies[i]] = prices[i]

    collection.insert_one({"stock_prices": stock_prices, "date": time.time()})
    time.sleep(3600)