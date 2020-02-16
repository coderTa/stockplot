import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import requests as r

response = r.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=compact&apikey=SES38O6CVHU3Z0XI")
data = response.json()



aapl_stock_prices = data["Time Series (Daily)"]
aapl_close_prices = []

for day in aapl_stock_prices:
    d = aapl_stock_prices[day]
    aapl_close_prices.append(float(d["4. close"]))

aapl_close_prices.reverse()

env_middle = []
time = []

for i in range(9, len(aapl_close_prices)):
    average = sum(aapl_close_prices[i - 9 : i + 1]) / 10
    env_middle.append(average)
    time.append(i)

env_middle = np.array(env_middle)

#print(appl_close_prices)

shift = 0.05

plt.fill_between(time, env_middle * (1 + shift), env_middle * (1 - shift), color = "#f5a04c55")

plt.plot(aapl_close_prices, linewidth = 4)
plt.plot(time, env_middle, linewidth = 2, color = "darkorange")
plt.plot(time, env_middle * (1 + shift), color = "yellow")
plt.plot(time, env_middle * (1 - shift), color = "orange")

plt.grid(True)

plt.show()