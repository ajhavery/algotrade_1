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
df.columns

idx = pd.IndexSlice
close = df.loc[idx[:],idx[:,'Close']]
# Getting all weekdays between 01/01/2000 and 12/31/2016
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
# Reindex close using all_weekdays as the new index as existing yahoo data may have missing values
close = close.reindex(all_weekdays)
close = close.fillna(method='ffill')
close = close.fillna(method='bfill')
close.to_csv('close.csv')

# EMA calculations and Buy Sell strategy
# Using Pandas to calculate a 20-days span EMA. adjust=False specifies that we are interested in the recursive calculation mode.
# When the price p(t) crosses the EMA(t)from below, close any existing short position and go long (buy) one unit of the asset.
# When the price p(t) crosses the EMA(t)from above, close any existing long position and go short (sell) one unit of the asset.
# i.e. in weight matrix
# Go long condition: If pi(t)> ei(t), then wi(t)=1/3
# Go short condition: If pi(t)< ei(t), then wi(t)=-1/3

short_rolling = close.rolling(window=20).mean()
ema_short = close.ewm(span=20, adjust=False).mean()
short_rolling.to_csv('shortrolling.csv')
ema_short.to_csv('emashort.csv')
# Taking the difference between the prices and the EMA timeseries
trading_positions_raw = close - ema_short
trading_positions_raw.to_csv('trading_position.csv')
trading_positions_raw.tail()
# Taking the sign of the difference to determine whether the price or the EMA is greater and then multiplying by 1/3
trading_positions = trading_positions_raw.apply(np.sign) * 1/3
trading_positions.head()
# To evaluate today's strategy, we need to look at previous day closing prices
# Action on t+1 will be driven by pricing data of t
# Lagging our trading signals by one day.
trading_positions_final = trading_positions.shift(1)
trading_positions_final.to_csv("tradingposfinal.csv")
trading_positions_final.head()

# Plotting Price, EMA and Trading positions
plot_start_date = '2018-01-01'
plot_end_date = '2019-01-20'

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,9))

ax1.plot(close.loc[plot_start_date:plot_end_date, :].index, close.loc[plot_start_date:plot_end_date, '^NSEI'], label='Price')
ax1.plot(ema_short.loc[plot_start_date:plot_end_date, :].index, ema_short.loc[plot_start_date:plot_end_date, '^NSEI'], label = 'Span 20-days EMA')
ax1.plot(short_rolling.loc[plot_start_date:plot_end_date, :].index, short_rolling.loc[plot_start_date:plot_end_date, '^NSEI'], label = '20-days SMA')

ax1.legend(loc='best')
ax1.set_ylabel('Price in ₹')
my_year_month_fmt = mdates.DateFormatter('%m-%y')
ax1.xaxis.set_major_formatter(my_year_month_fmt)

ax2.plot(trading_positions_final.loc[plot_start_date:plot_end_date, :].index, trading_positions_final.loc[plot_start_date:plot_end_date, '^NSEI'],
         label='Trading position')
ax2.set_ylabel('Trading position')
ax2.xaxis.set_major_formatter(my_year_month_fmt)

# Effective returns of the strategy is as calculated below:
# Log returns - First the logarithm of the prices is taken and the the difference of consecutive (log) observations
asset_log_returns = np.log(close).diff()
asset_log_returns.to_csv("log_returns.csv")
asset_log_returns.head()

strategy_asset_log_returns = trading_positions_final * asset_log_returns
strategy_asset_log_returns.to_csv("StartegyLogReturns.csv")
strategy_asset_log_returns.head()

# Get the cumulative log-returns per asset and Transform the cumulative log returns to relative returns
cum_strategy_asset_log_returns = strategy_asset_log_returns.cumsum()
cum_strategy_asset_log_returns.to_csv("CumAssetLogReturns.csv")
cum_strategy_asset_relative_returns = np.exp(cum_strategy_asset_log_returns) - 1
cum_strategy_asset_relative_returns.to_csv("CumStartegyRelReturns.csv")

#Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,9))

for c in asset_log_returns:
    ax1.plot(cum_strategy_asset_log_returns.loc[plot_start_date:plot_end_date, :].index, cum_strategy_asset_log_returns.loc[plot_start_date:plot_end_date, c], label=str(c[0]))

ax1.set_ylabel('Cumulative log-returns')
ax1.legend(loc='best')
ax1.xaxis.set_major_formatter(my_year_month_fmt)

for c in asset_log_returns:
    ax2.plot(cum_strategy_asset_relative_returns.loc[plot_start_date:plot_end_date, :].index, 100*cum_strategy_asset_relative_returns.loc[plot_start_date:plot_end_date, c], label=str(c[0]))

ax2.set_ylabel('Total relative returns (%)')
ax2.legend(loc='best')
ax2.xaxis.set_major_formatter(my_year_month_fmt)

# Total strategy relative returns. This is the exact calculation.
cum_relative_return_exact = cum_strategy_asset_relative_returns.sum(axis=1)
# Get the cumulative log-returns per asset
# axis = 0 => sum along the rows; axis = 1 => sum along the columns
cum_strategy_log_return = cum_strategy_asset_log_returns.sum(axis=1)
# Transform the cumulative log returns to relative returns. This is the approximation
cum_relative_return_approx = np.exp(cum_strategy_log_return) - 1
#To CSV
cum_relative_return_exact.to_csv("CumReturnsExact.csv")
cum_strategy_log_return.to_csv("CumStartegyLogReturns.csv")
cum_relative_return_approx.to_csv("CumReturnsApprox.csv")

# Plot to compare exact and approximate relative return
fig, ax = plt.subplots(figsize=(16,9))

ax.plot(cum_relative_return_exact.index, 100*cum_relative_return_exact, label='Exact')
ax.plot(cum_relative_return_approx.index, 100*cum_relative_return_approx, label='Approximation')

ax.set_ylabel('Total cumulative relative returns (%)')
ax.legend(loc='best')
ax.xaxis.set_major_formatter(my_year_month_fmt)