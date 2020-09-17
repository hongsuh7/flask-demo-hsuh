import requests
from datetime import datetime

apikey = 'XXMWEDAIC3RFSRO3'

symbol = 'IBM'

request_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + apikey

r = requests.get(request_url)
r_json = r.json()
print(r_json)
print(len(r_json))

ts = r_json['Time Series (Daily)']

dates = []
closing_prices = []

for date in ts:
    dates.append(datetime.strptime(date, "%Y-%m-%d"))
    closing_prices.append(float(ts[date]['4. close']))

print(dates[:6])
print(closing_prices[:6])