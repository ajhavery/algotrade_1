# This file is strategy #1 including use of moving averages to draw buy/sell strategy
# Exponential Moving average
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import fix_yahoo_finance as yf
import seaborn as sns
plt.rcParams.update({'font.size': 7})

# SMA series come with lag of L days
# Average Lag (L) = M/2; i.e. for 100 days SMA, avg lag = 100/2 = 50 days
# Exponential Moving Average (EMA), defined as
# EMA(t) = (1−α)EMA(t−1)+α p(t)
# EMA(t_0) = p(t_0)
# α = 1/(L+1)
# α = 2/(M+1)

symbol = ['^NSEI', '^BSESN', 'SBIN.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'TATAMOTORS.NS', 'MARUTI.NS']
start_date = '2009-01-01'
end_date = '2019-01-23'
yf.pdr_override()
df = pdr.get_data_yahoo(symbol, start_date, end_date, group_by = 'ticker', auto_adjust = True, thread = 5)
df.head(5)