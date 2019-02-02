#web scrapping code to get list of all companies which are part of NSE
# list: https://www.moneyworks4me.com/best-index/nse-stocks/top-nse500-companies-list

import bs4 as bs
import pickle # pickle serializes any python object
import requests

def save_nse100_tickers():
    resp = requests.get('https://www.moneycontrol.com/stocks/marketinfo/marketcap/nse/index.html')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'tbldata14 bdrtpg'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('a')[0].text
        tickers.append(ticker)

    with open("C:/Users/ankur.jhavery/PycharmProjects/algotrade_1/pickle/nse100tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

save_nse100_tickers()

# Yahoo tickers are downloaded using Yahootickerdownloader.py; then fuzzy lookup with names loaded in this function

