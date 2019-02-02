#web scrapping code to get list of all companies which are part of NSE
# list: https://www.moneyworks4me.com/best-index/nse-stocks/top-nse500-companies-list

import bs4 as bs
import pickle # pickle serializes any python object
import requests
import datetime as dt
import fix_yahoo_finance as yf
from pandas_datareader import data as pdr
import os
import pandas as pd

def save_nse100_tickers():
    resp = requests.get('https://www.moneycontrol.com/stocks/marketinfo/marketcap/nse/index.html')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'tbldata14 bdrtpg'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('a')[0].text
        tickers.append(ticker)

    with open("pickle/nse100tickers.pickle", "wb") as f: #write bytes
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

#save_nse100_tickers()
# commented since already downloaded

def get_data_from_yahoo(symbol,no_of_tickers,ticker_override = False,reload_nse100 = False,update = False):
    if ticker_override:
        tickers = symbol
    else:
        if reload_nse100:
            tickers = save_nse100_tickers()
        else:
            with open("pickle/nse100tickers.pickle", "rb") as f:  # read bytes
                tickers = pickle.load(f)

    if update:
        start_date = dt.datetime(2000, 1, 1)
        end_date = dt.datetime(2019, 1, 31)
        yf.pdr_override()
        if not os.path.exists('stock_csvs'):
            os.makedirs('stock_csvs')

        for ticker in tickers[:no_of_tickers]:  #first 20 symbols only
            if not os.path.exists('stock_csvs/{}.csv'.format(ticker)):
                df = pdr.get_data_yahoo(ticker, start_date, end_date, group_by='ticker', auto_adjust=True, thread=5)
                df.to_csv('stock_csvs/{}.csv'.format(ticker))
            else:
                print('Data exists for {}'.format(ticker))

symbol = ['^NSEI','RELIANCE.NS','TCS.NS','HDFCBANK.NS','HINDUNILVR.NS','ITC.NS','HDFC.NS','INFY.NS','SBIN.NS', \
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

get_data_from_yahoo(symbol,20,True,False,True)

def compile_data(symbol,no_of_tickers):
    main_df = pd.DataFrame()
    for count,ticker in enumerate(symbol[:no_of_tickers]):
        df = pd.read_csv('stock_csvs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        df.rename(columns = {'Close':ticker},inplace= True)
        df.drop(['Open','High','Low','Volume'],1,inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 5 == 0:
            print(count) # track of how many joins are done
    print(main_df.head())
    main_df.to_csv('stock_csvs/nseTop%d.csv' % no_of_tickers)

compile_data(symbol,10)

