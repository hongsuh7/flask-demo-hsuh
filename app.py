from flask import Flask, render_template, request, redirect
import simplejson as json
import requests
from datetime import datetime
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
app = Flask(__name__)


apikey = 'XXMWEDAIC3RFSRO3'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # tidy the request form
        symbol = request.form['symbol'].upper()
        if 'open' in request.form:
            opening = request.form['open']
        else:
            opening = "off"
        if 'close' in request.form:
            closing = request.form['close']
        else:
            closing = "off"

        # generate request string
        request_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + apikey

        # make the request and receive in json
        r = requests.get(request_url)
        r_json = r.json()

        if 'Error Message' in r_json:
            return render_template('index.html', msg=r_json['Error Message'])

        ts = r_json['Time Series (Daily)']

        dates = []
        opening_prices = []
        closing_prices = []

        # extract data
        if closing == "on":
            for date in ts:
                dates.append(datetime.strptime(date, "%Y-%m-%d"))
                closing_prices.append(float(ts[date]['4. close']))
        if opening == "on":
            for date in ts:
                dates.append(datetime.strptime(date, "%Y-%m-%d"))
                opening_prices.append(float(ts[date]['1. open']))

        # create the plot
        p = figure(title=symbol, x_axis_label='Date', y_axis_label='Price (dollars)', x_axis_type='datetime')
        p.line(dates, closing_prices, line_width=2, line_color='blue', alpha=0.6, legend_label="Closing price")
        p.line(dates, opening_prices, line_width=2, line_color='red', alpha=0.6, legend_label="Opening price")
        p.legend.location = "top_left"
        plot = file_html(p, CDN, 'plot')

        return render_template('index.html', plot=plot)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=33507)
