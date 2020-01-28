from pymongo import MongoClient
import matplotlib.pyplot as plt
import pytz
from datetime import datetime
import numpy as np

mc = MongoClient("mongodb://techster_ben:Iltcvm50!@techsterben-cluster-shard-00-00-zx79j.gcp.mongodb.net:27017,techsterben-cluster-shard-00-01-zx79j.gcp.mongodb.net:27017,techsterben-cluster-shard-00-02-zx79j.gcp.mongodb.net:27017/test?ssl=true&replicaSet=TechsterBen-Cluster-shard-0&authSource=admin&retryWrites=true")
#print(mc.list_databases())

#for db in mc.list_databases():
    #print(db)

stocks_database = mc.Stocks
popular_stocks = stocks_database.Popular_stocks

#print(popular_stocks.find())

appl_stock_prices = []

tz = pytz.timezone('US/Pacific')

for stock in popular_stocks.find():
    #print(stock['stock_prices'])
    date = stock['date']
    date = datetime.fromtimestamp(date, tz)

    #if 13 > date.hour >= 7 or (date.hour == 6 and date.minute >= 30):
    if date.hour == 13:    
        if date.weekday() not in [5, 6]:
            appl_stock_prices.append(float(stock['stock_prices']['Apple']))
    


env_middle = []
time = []

for i in range(9, len(appl_stock_prices)):
    average = sum(appl_stock_prices[i - 9 : i + 1]) / 10
    env_middle.append(average)
    time.append(i)

env_middle = np.array(env_middle)

#print(appl_stock_prices)

shift = 0.05

plt.fill_between(time, env_middle * (1 + shift), env_middle * (1 - shift), color = "#f5a04c55")

plt.plot(appl_stock_prices, linewidth = 4)
plt.plot(time, env_middle, linewidth = 2, color = "darkorange")
plt.plot(time, env_middle * (1 + shift), color = "yellow")
plt.plot(time, env_middle * (1 - shift), color = "orange")

plt.grid(True)

plt.show()