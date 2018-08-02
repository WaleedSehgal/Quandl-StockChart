# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 20:02:23 2018

@author: Waleed
"""

import io
import quandl
import base64
import matplotlib.pyplot as plt
quandl.ApiConfig.api_key = 'zC992yeEkw5VTye5PFJY'

from flask import Flask, render_template

server = Flask(__name__)

@server.route('/')
def stockAAPL():
    
    #retrieve stock data from quandl
    data = quandl.get('WIKI/AAPL', collapse = 'monthly')
    plt.style.use("ggplot")
    
    #average of 99 days price
    data['100mean'] = data['Adj. Close'].rolling(window=100, min_periods=0).mean()
    
    #I have created two plots in a single graph here
    axis1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    axis2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1)
    
    axis1.plot(data.index, data['Adj. Close'])
    axis1.plot(data.index, data['100mean'])
    axis1.plot(data.index, data['High'])
    
    axis2.plot(data.index, data['Volume'])
    
    img = io.BytesIO()
   
    plt.plot()
    plt.savefig(img, format='png')
    img.seek(0)
    
    #encode the image
    plot_url = base64.b64encode(img.getvalue())

    return render_template('index.html', plot_url=plot_url.decode('utf8'))


if __name__ == "__main__":
    server.run(debug=True, port=7777)   
    