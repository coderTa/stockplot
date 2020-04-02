# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import requests as r
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from datetime import datetime

#stock_names = ["AAPL", "NIO", "BABA", "LK", "CLDR", "MNDB"]

# Failed attempt at Alpha Vantage api - they don't allow enough pulled requests per minute
"""
for stock in stock_names:
    response = r.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=compact&apikey=SES38O6CVHU3Z0XI" % stock)

    stock_data = response.json()
    print(str(stock_data)[:300])
    stock_data = stock_data['Time Series (Daily)']

    print(stock_data)

    close_values = []

    for day in stock_data:
        close_values.append(float(stock_data[day]['4. close']))

    #print(response.json())
    print(stock)
    print(close_values)
"""

c = MongoClient("mongodb://techster_ben:Iltcvm50!@techsterben-cluster-shard-00-00-zx79j.gcp.mongodb.net:27017,techsterben-cluster-shard-00-01-zx79j.gcp.mongodb.net:27017,techsterben-cluster-shard-00-02-zx79j.gcp.mongodb.net:27017/test?ssl=true&replicaSet=TechsterBen-Cluster-shard-0&authSource=admin&retryWrites=true")
collection = c.Stocks.SP500


name_to_price = {}

for page in range(1, 11):
    data = r.get("https://markets.businessinsider.com/index/components/s&p_500?p=%d" % page)
    b = bs(data.text, 'html.parser')

    rows = b.find_all("tr")
    #print(rows)
    for row in rows[1:]:
        cells = row.find_all('td')
        if cells:
            name_to_price[cells[0].get_text()[1:]] = float(cells[1].get_text().split('\n')[1].replace(',', ''))
            #print(cells[0].get_text())
            print(float(cells[1].get_text().split('\n')[1].replace(',', '')))

    print("loaded pg %d" % page)
    #print(len(rows))

data_array = []

if datetime.today().weekday() not in [5, 6]:
    for name in name_to_price:
        document = {
            "name" : name[:-1],
            "stockPrice" : name_to_price[name],
            "date" : str(datetime.today())
        }

        data_array.append(document)

    print(collection.insert_many(data_array))

documents = collection.find().sort("date", -1)

name_to_history = {}

for d in documents:
    if d["name"] in name_to_history:
        name_to_history[d["name"]].append(d["stockPrice"])
    else:
        name_to_history[d["name"]] = [d["stockPrice"]]

running_avg_crossed = []
increase_ten = []
decrease_ten = []
under_avg_crossed = []

for stock in name_to_history:
    if len(name_to_history[stock]) > 10:
        history = name_to_history[stock]
        running_avg = sum(history[-10:]) / 10
        under_avg = running_avg * 0.9

        if history[-1] > running_avg and history[-2] < running_avg:
            running_avg_crossed.append(stock)

        if history[-1] < under_avg and history[-2] > under_avg:
            under_avg_crossed.append(stock)

        if history[-1] / history[-2] > 1.1:
            increase_ten.append(stock)

        if history[-1] / history[-2] < 0.9:
            decrease_ten.append(stock)

message = Mail(
    from_email='yeet@yeet.com',
    to_emails='benjamin.ta@yahoo.com',
    subject='Stock prices updates:',
    html_content="""
    <strong>Stock updates for %s</strong>
    <p>Stocks that crossed running average: %s</p>
    <p>Stocks that dropped below bottom envelope: %s</p>
    <p>Stocks that increased 10 percent or more: %s</p>
    <p>Stocks that decreased 10 percent or more: %s</p>
    """ % datetime.today(), running_avg_crossed, under_avg_crossed, increase_ten, decrease_ten)
try:
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    #print(response.body)
    #print(response.headers)
except Exception as e:
    print(e.message)

#print(name_to_history)
#print(name_to_price)
#print(len(name_to_price))