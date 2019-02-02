from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import datetime as dt

# Data download from yahoo finance
#BSE = '^BSESN'
symbol = ['^NSEI','RELIANCE.NS','TCS.NS','HDFCBANK.NS','HINDUNILVR.NS','ITC.NS','HDFC.NS','INFY.NS','SBIN.NS', \
          'KOTAKBANK.NS','ICICIBANK.NS','MARUTI.NS','LT.NS','AXISBANK.NS','ONGC.NS','WIPRO.NS','BAJAJFINANCE.NS', \
          'HCLTECH.NS','ASIANPAINT.NS','COALINDIA.NS','IOC.NS','BHARTIARTL.NS','NTPC.NS','NESTLEIND.NS','HINDZINC.NS', \
          'SUNPHARMA.NS','POWERGRID.NS','BAJAJFINSV.NS','ULTRACEMCO.NS','INDUSINDBK.NS','TITAN.NS','M&M.NS','DABUR.NS', \
          'BRITANNIA.NS','HDFCLIFE.NS','BAJAJ-AUTO.NS','GAIL.NS','BPCL.NS','TECHM.NS','GODREJCP.NS','ADANIPORTS.NS', \
          'JSWSTEEL.NS','VEDL.NS','SBILIFE.NS','BOSCHLTD.NS','TATASTEEL.NS','PIDILITIND.NS','HEROMOTOCO.NS','SHREECEM.NS', \
          'INFRATEL.NS','EICHERMOT.NS','TATAMOTORS.NS','MARICO.NS','BANDHANBNK.NS','HINDALCO.NS','GRASIM.NS','AUROPHARMA.NS',\
          'DRREDDY.NS','HAVELLS.NS','INDOGO.NS','MOTHERSUMI.NS','GICRE.NS','YESBANK.NS','AMBUJACEM.NS','CIPLA.NS','ICICIPRULI.NS',\
          'IDBI.NS','DIVISLABS.NS','CONCOR.NS','BIOCON.NS','ICICIGI.NS','LUPIN.NS','UPL.NS','PEL.NS','MCDOWELL-N.NS','UBL.NS', \
          'SIEMENS.NS','HINDPETRO.NS','COLPAL.NS','ZEEL.NS','PETRONET.NS','CADILAHC.NS','OFSS.NS','PGHH.NS','BAJAJHLDNG.NS','BERGERPAINT.NS',\
          'GSKCONS.NS','LT.NS','TORNTPHARM.NS','NMDC.NS','DLF.NS','BANKBARODA.NS','IBULHSGFIN.NS','NIACL.NS','HDFCAMC.NS','PNB.NS',\
          'PFC.NS','IDEA.NS','ABB.NS' ]
start_date = dt.datetime(2000,1,1)
end_date = dt.datetime(2019,1,31)
yf.pdr_override()
df = pdr.get_data_yahoo(symbol, start_date, end_date, group_by = 'ticker', auto_adjust = True, thread = 5)
df.head(5)
df.to_csv('csv/NSE100quotes.csv')