# import fix_yahoo_finance as yf
# df = yf.download(symbol, start_date, end_date)

from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
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

df.to_csv('NSE.csv')
df.head(5)
df.columns

idx = pd.IndexSlice
#Getting only closing prices
close = df.loc[idx[:],idx[:,'Close']]
# Getting all weekdays between 01/01/2000 and 12/31/2016
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
# Reindex close using all_weekdays as the new index as existing yahoo data may have missing values
close = close.reindex(all_weekdays)
# Reindexing will insert missing values (NaN) for the dates that were not present in the original set.
# We can fill the missing values by replacing them with the latest available price for each instrument.
# method : {‘backfill’, ‘bfill’, ‘pad’, ‘ffill’, None}, default None
# pad / ffill: propagate last valid observation forward to next valid
# backfill / bfill: use NEXT valid observation to fill gap
close = close.fillna(method='ffill')
close = close.fillna(method='bfill')

close.head(5)
close.describe()

#getting close price data
nse = close.loc[idx[:],idx['^NSEI', :]]
bse = close.loc[idx[:],idx['^BSESN', :]]
sbi = close.loc[idx[:],idx['SBIN.NS', :]]
hdfc = close.loc[idx[:],idx['HDFCBANK.NS', :]]
icici = close.loc[idx[:],idx['ICICIBANK.NS', :]]
tatamotors = close.loc[idx[:],idx['TATAMOTORS.NS', :]]
maruti = close.loc[idx[:],idx['MARUTI.NS', :]]

# Calculate the 20 and 100 days moving averages of the closing prices
short_rolling_nse = nse.rolling(window=20).mean()
long_rolling_nse = nse.rolling(window=100).mean()
short_rolling_bse = bse.rolling(window=20).mean()
long_rolling_bse = bse.rolling(window=100).mean()
short_rolling_sbi = sbi.rolling(window=20).mean()
long_rolling_sbi = sbi.rolling(window=100).mean()
short_rolling_hdfc = hdfc.rolling(window=20).mean()
long_rolling_hdfc = hdfc.rolling(window=100).mean()
short_rolling_icici = icici.rolling(window=20).mean()
long_rolling_icici = icici.rolling(window=100).mean()
short_rolling_tata = tatamotors.rolling(window=20).mean()
long_rolling_tata = tatamotors.rolling(window=100).mean()
short_rolling_maruti = maruti.rolling(window=20).mean()
long_rolling_maruti = maruti.rolling(window=100).mean()

# Plot everything by leveraging the very powerful matplotlib package







fig, ax = plt.subplots(figsize=(16,9))
ax.plot(nse.index, nse, label='NSE')
ax.plot(short_rolling_nse.index, short_rolling_nse, label='20 days rolling')
ax.plot(long_rolling_nse.index, long_rolling_nse, label='100 days rolling')

ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price')
ax.legend(loc='best')

fig, by = plt.subplots(figsize=(16,9))
by.plot(bse.index, bse, label='BSE')
by.plot(short_rolling_bse.index, short_rolling_bse, label='20 days rolling')
by.plot(long_rolling_bse.index, long_rolling_bse, label='100 days rolling')

by.set_xlabel('Date')
by.set_ylabel('Adjusted closing price')
by.legend()

# normal returns = p(t)/p(t-1)
returns = close.pct_change(1)
returns.head()

# Log returns - First the logarithm of the prices is taken and the the difference of consecutive (log) observations
log_returns = np.log(close).diff()
log_returns.describe()

# plotting returns
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,12))

for c in log_returns:
    ax1.plot(log_returns.index, log_returns[c].cumsum(), label=str(c[0]))
ax1.set_ylabel('Cumulative log returns')
ax1.legend(loc='best')

for c in log_returns:
    ax2.plot(log_returns.index, 100*(np.exp(log_returns[c].cumsum()) - 1), label=str(c[0]))
ax2.set_ylabel('Total relative returns (%)')
ax2.legend(loc='best')

plt.show()

#Making buy sell decision
#Making last day returns a column vector

log_returns.head(5)
weights_matrix = pd.DataFrame(1 / 3, index=close.index, columns=close.columns)
weights_matrix.describe()
weights_matrix.head(5)
# Calculating portfolio return
# Initially the two matrices are multiplied. Note that we are only interested in the diagonal,
# which is where the dates in the row-index and the column-index match.
temp_var = weights_matrix.dot(log_returns.transpose())
temp_var.head().iloc[:, 0:5]
temp_var.describe()
temp_var

# The numpy np.diag function is used to extract the diagonal and then
# a Series is constructed using the time information from the log_returns index
portfolio_log_returns = pd.Series(np.diag(temp_var), index=log_returns.index)
# The below will also work. A dataframe is a collection of series
# portfolio_log_returns = pd.DataFrame(np.diag(temp_var), index=log_returns.index)
portfolio_log_returns.tail()

# Sum of all log returns gives the portfolio log return over the period
# log_return = log (p_t/p_0)
# p_t/p_0 = e ^ log_return
# % return = (p_t - p_0)/p_0 = e ^ log_return - 1
total_relative_returns = (np.exp(portfolio_log_returns.cumsum()) - 1)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,12))

ax1.plot(portfolio_log_returns.index, portfolio_log_returns.cumsum())
ax1.set_ylabel('Portfolio cumulative log returns')

ax2.plot(total_relative_returns.index, 100 * total_relative_returns)
ax2.set_ylabel('Portfolio total relative returns (%)')

plt.show()

# Calculating the time-related parameters of the simulation
days_per_year = 52 * 5
total_days_in_simulation = close.shape[0]
number_of_years = total_days_in_simulation / days_per_year

# The last data point will give us the total portfolio return
total_portfolio_return = total_relative_returns[-1]
# Average portfolio return assuming compunding of returns
average_yearly_return = (1 + total_portfolio_return)**(1 / number_of_years) - 1

print('Total portfolio return is: ' +
      '{:5.2f}'.format(100 * total_portfolio_return) + '%')
print('Average yearly return is: ' +
      '{:5.2f}'.format(100 * average_yearly_return) + '%')