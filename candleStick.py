# Making candlestick chart
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

style.use('ggplot')
plt.rcParams.update({'font.size': 7})

# Data download from yahoo finance
symbol = ['^NSEI', '^BSESN', 'SBIN.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'TATAMOTORS.NS', 'MARUTI.NS']
start_date = dt.datetime(2009,1,1)
end_date = dt.datetime(2019,1,31)
yf.pdr_override()
df = pdr.get_data_yahoo(symbol, start_date, end_date, group_by = 'ticker', auto_adjust = True, thread = 5)
df.head(5)
idx = pd.IndexSlice
HDFC = df.loc[idx[:],idx['HDFCBANK.NS',:]]
HDFC.columns = HDFC.columns.droplevel()
HDFC.to_csv('HDFCstockQuotes.csv')

# if we need date as a column, don't ask to parse dates in col 0 as index
# HDFCquotes = pd.read_csv('HDFCstockQuotes.csv')
HDFCquotes = pd.read_csv('HDFCstockQuotes.csv', parse_dates= True, index_col = 0)

# resample aggregates 10 day block data in 1 set; not rolling
hdfc_ohlc = HDFCquotes.resample('10D').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'})
hdfc_ohlc.head(5)
# candlestick_ohlc wants from us dates in mdates format and Open, high, low and close
hdfc_ohlc.reset_index(inplace=True)
hdfc_ohlc.head(5)
# convert normal dates to matplot mdates
hdfc_ohlc['Date'] = hdfc_ohlc['Date'].map(mdates.date2num)

#Setting figures
fig, ax1 = plt.subplots(figsize=(16,9))
ax1.xaxis_date()

candlestick_ohlc(ax1, hdfc_ohlc.values, width=4, colorup='g', colordown='r')