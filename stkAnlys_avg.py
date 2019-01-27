from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import fix_yahoo_finance as yf
import seaborn as sns
plt.rcParams.update({'font.size': 7})

symbol = ['^NSEI', '^BSESN', 'SBIN.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'TATAMOTORS.NS', 'MARUTI.NS']
start_date = '2009-01-01'
end_date = '2019-01-23'
yf.pdr_override()
df = pdr.get_data_yahoo(symbol, start_date, end_date, group_by = 'ticker', auto_adjust = True, thread = 5)
df.head(5)
df.columns

idx = pd.IndexSlice
close = df.loc[idx[:],idx[:,'Close']]
# Getting all weekdays between 01/01/2000 and 12/31/2016
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
# Reindex close using all_weekdays as the new index as existing yahoo data may have missing values
close = close.reindex(all_weekdays)
close = close.fillna(method='ffill')
close = close.fillna(method='bfill')
close.head(5)
close.describe()

short_rolling = close.rolling(window=20).mean()
long_rolling = close.rolling(window=100).mean()
short_rolling.head(20)
long_rolling.head(100)

# SMA (short moving average) prices are much less noisy but trend can be seen with a lag

