import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style

##start = dt.datetime(2000,1,1)
##end = dt.datetime(2020, 12, 31)
##
##df = web.DataReader('TSLA', 'yahoo', start, end)
##df.to_csv('tsla.csv')

style.use('ggplot')

df = pd.read_csv('tsla.csv', index_col=0, parse_dates=True)

df['Adj Close'].plot()
plt.show()
