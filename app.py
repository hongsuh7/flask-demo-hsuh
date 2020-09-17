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
        # generate request string
        symbol = request.form['symbol']
        request_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + apikey

        # make the request and receive in json
        r = requests.get(request_url)
        r_json = r.json()

        if 'Error Message' in r_json:
            return render_template('index.html', msg=r_json['Error Message'])

        ts = r_json['Time Series (Daily)']

        dates = []
        closing_prices = []

        # extract data
        for date in ts:
            dates.append(datetime.strptime(date, "%Y-%m-%d"))
            closing_prices.append(float(ts[date]['4. close']))

        p = figure(title=symbol, x_axis_label='Time', y_axis_label='Price (dollars)', x_axis_type='datetime')
        p.line(dates, closing_prices, line_width=2)

        plot = file_html(p, CDN, 'plot')

        return render_template('index.html', plot=plot)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=33507)
