import pickle
import bs4 as bs
import requests
import datetime as dt
import os
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import time

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text[:-1]
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)

    return tickers

def get_data_from_yahoo(reload_sp500_ticker=False, reload_sp500_data=False):
    if reload_sp500_ticker:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
            os.makedirs('stock_dfs')


##    start = dt.datetime(2000, 1, 1)
##    end = dt.datetime(2020, 12, 31)

    if reload_sp500_data or not os.path.exists('stock_dfs/sp500data.csv'):
        ticker_string = ''
        for ticker in tickers:
            ticker_string += ' ' + ticker

        data = yf.download(tickers = ticker_string, period="10y",
                       interval="1d", group_by='ticker', auto_adjust = True,
                       thread = True)
        data.to_csv('stock_dfs/sp500data.csv')

    else:
        print('Already have data')
            
        

get_data_from_yahoo()
