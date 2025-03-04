## This program is used to gather s&p500 stock data and calculates correlation between them

import pickle
import bs4 as bs
import requests
import datetime as dt
import os
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import time
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot') # Sets style for matplotlib

# Collects, stores and returns names of all s&p500 company tickers
# effects: produces output
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

# collects and stores data for all collected s&p500 tickers from yahoo
# reload_sp500_ticker - Set to True to reload names of s&p500 tickers
# reload_sp500_data - Set to True to reload s&p500 data
# effects: produces output
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

    if reload_sp500_data or not os.path.exists('stock_dfs/sp500data.pickle'):
        ticker_string = ''
        for ticker in tickers:
            ticker_string += ' ' + ticker

        data = yf.download(tickers = ticker_string, period="10y", 
            group_by='ticker', thread = True)

        data.to_pickle('stock_dfs/sp500data.pickle')

    else:
        print('Already have data')
            
# creates and stores table of s&p 500 Adj close data joined together in one table            
def create_joined_table():
    if not os.path.exists('stock_dfs/sp500data.pickle'):
        print('Data does not exist')
        return

    with open('stock_dfs/sp500data.pickle', 'rb') as f:
        data = pd.read_pickle(f)

    main_dfs = pd.DataFrame()

    for (ticker, col) in data:
        if(col == 'Adj Close'):
            stock_dfs = data[ticker]
            stock_dfs.rename(columns = {'Adj Close': ticker}, inplace=True)
            stock_dfs.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

            if(main_dfs.empty):
                main_dfs = stock_dfs
            else:
                main_dfs = main_dfs.join(stock_dfs, how="outer")

    main_dfs.to_csv('stock_dfs/sp500close.csv')
    # for key in data['MSFT'].keys():
    #     print(key)

# Calculates correlation between Adj close prices and creates a corresponding heatmap.
def visualize_data():
    if not os.path.exists('stock_dfs/sp500close.csv'):
        print('Data does not exist')
        return

    main_dfs = pd.read_csv('stock_dfs/sp500close.csv')
    main_dfs.set_index('Date', inplace=True) 
    # corr_dfs = main_dfs.pct_change().corr()
    corr_dfs = main_dfs.corr()
    filter_negative_correlation(corr_dfs)
    # corr_dfs.to_csv('analysis/price_correlation/price_corr.csv')

    sns.heatmap(corr_dfs,cmap='RdYlGn', xticklabels=True, yticklabels=True)
    plt.show()
    

# Takes in a correlation table and filters out the negatively correlated stocks
def filter_negative_correlation(corr_dfs):
    mean_corr = corr_dfs.mean()
    print(mean_corr.where(mean_corr.values < 0).dropna())

# get_data_from_yahoo()
# create_joined_table()
visualize_data()
