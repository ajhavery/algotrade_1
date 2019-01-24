from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import pandas as pd

import fix_yahoo_finance as yf
yf.pdr_override()

symbol = ['NSE', 'BSE']
start_date = '2010-01-01'
end_date = '2019-01-24'
df = pdr.get_data_yahoo(symbol, start_date, end_date, group_by = 'ticker', auto_adjust = True, thread = 5)
#below can also be used
#df = yf.download(symbol, start="2017-01-01", end="2017-04-30")

#df.to_csv('NSE.csv')
df.head(5)
df.columns

idx = pd.IndexSlice
close = df.loc[idx[:],idx['NSE','Close']]

close.head(5)