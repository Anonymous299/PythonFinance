import pandas as pd
import numpy as np
from collections import Counter

# Preprocess stock data for machine learning algorithm
# Creates column which calculates pct change in stock upto 7 days
def preprocess_stock_data(ticker):
	
	period = 7
	main_dfs = pd.read_csv('stock_dfs/sp500close.csv', index_col=0)
	tickers = main_dfs.columns.values.tolist()
	main_dfs.fillna(0, inplace=True)

	for i in range(1, period + 1):
		main_dfs['{}_{}d'.format(ticker, i)] = (main_dfs[ticker].shift(-i) - main_dfs[ticker]) / main_dfs[ticker]

	# print(main_dfs.head(15))
	return tickers, main_dfs, period

# Proxy function to classify stock as buy, sell or hold according 
# to pct change in the next 7 days
def buy_sell_hold(*args):
	cols = [c for c in args]
	req = 0.02

	for col in cols:
		if col > req:
			return 1
		if col < -req:
			return -1
	return 0

# Build buy, sell and hold feature column for ticker
def extract_featureset(ticker):
	tickers, df, period = preprocess_stock_data(ticker)
	df['{}_rating'.format(ticker)] = list(map(buy_sell_hold, *[df['{}_{}d'.format(ticker, i)] for i in range(1, period+1)]))
	
	# Calculating spread of ratings
	vals = df['{}_rating'.format(ticker)].values.tolist()
	str_vals = [str(i) for i in vals]
	print('Rating spread:', Counter(str_vals))
	df.fillna(0, inplace=True)

	df = df.replace([np.inf, -np.inf], np.nan)
	df.dropna(inplace=True)

	df_vals = df[[ticker for ticker in tickers]].pct_change()
	df_vals = df_vals.replace([np.inf, -np.inf], 0)
	df_vals.fillna(0, inplace=True)

	X = df_vals.values
	y = df['{}_rating'.format(ticker)].values

	return X, y, df

# preprocess_stock_data('AAPL')
extract_featureset('AAPL')