import time
import csv
import json

import requests
from random import randint

def get_request(u):
    '''
    This is meant to be a utility function to complete a get request
    input: {u: url}
    output request.response()
    '''
    count = 0
    while count < 10:
        try:
            r = requests.get(u)
            count = 10
        except:
            count += 1
            time.sleep(randint(1,5))
    return r


def get_otc_tickers(l="http://otcmarkets.com/research/stock-screener/api/downloadCSV", ticker_price=5):
    '''
    Quick and dirty function to get all of the otc tickers from otc markets
    ** This has not been vetted and it is unknown whether this list is comprehensive
    '''
    # l = "http://otcmarkets.com/research/stock-screener/api/downloadCSV"
    r = get_request(l)
    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    cr_list = list(cr)[1:]
    tickers = [x[0] for x in cr_list if float(x[3]) < ticker_price]
    prices = [float(x[3]) for x in cr_list if float(x[3]) < ticker_price]

    return tickers, prices


def get_ticker_json(ticker):
    url = f"https://backend.otcmarkets.com/otcapi/company/profile/full/{ticker}"
    r = get_request(url)
    # r = requests.get(url)
    ticker_json = r.json()
    return ticker_json
