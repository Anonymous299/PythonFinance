import pandas as pd

# Preprocess stock data for machine learning algorithm
# Creates column which calculates pct change in stock upto 7 days
def preprocess_stock_data(ticker):
	
	period = 7
	main_dfs = pd.read_csv('stock_dfs/sp500close.csv', index_col=0)
	tickers = main_dfs.columns.values.tolist()
	main_dfs.fillna(0, inplace=True)

	for i in range(1, period + 1):
		main_dfs['{}_{}d'.format(ticker, i)] = (main_dfs[ticker].shift(-i) - main_dfs[ticker]) / main_dfs[ticker]

	print(main_dfs)
	return tickers, main_dfs

df = preprocess_stock_data('AAPL')