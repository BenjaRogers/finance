import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd

symbol_list = pd.read_csv('bats_symbols.csv')
yf.pdr_override()


EMA_USED = [3,5,8,10,12,15,30,40,45,50,60]
now = dt.datetime.now()
start = dt.datetime(now.year-1, now.month, now.day)

def get_rwb_list(ticker_symbols):
    rwb_is_true_list = []
    for symbol in symbol_list.index:
        symbol_name = str(symbol_list["Name"][symbol])
        df = pdr.get_data_yahoo(symbol_name, start, now)

        #create new columns with ema ranges
        for x in EMA_USED:
            df["ema_"+str(x)] = round(df.iloc[:,4].ewm(span=x, adjust=False).mean(),2)

        today_cmin = min(df['ema_3'][-1], df['ema_5'][-1], df['ema_8'][-1], df['ema_12'][-1], df['ema_15'][-1])
        today_cmax = max(df['ema_30'][-1], df['ema_40'][-1], df['ema_45'][-1], df['ema_50'][-1], df['ema_60'][-1])

        yesterday_cmin = min(df['ema_3'][-2], df['ema_5'][-2], df['ema_8'][-2], df['ema_12'][-2], df['ema_15'][-2])
        yesterday_cmax = max(df['ema_30'][-2], df['ema_40'][-2], df['ema_45'][-2], df['ema_50'][-2], df['ema_60'][-2])

        #This is the threshold to suggest moving into a buy position for whatever stock meets this condition
        if today_cmin > today_cmax and yesterday_cmin < yesterday_cmax:
            print(symbol_name + " is rwb")
            print(today_cmin, today_cmax)
            rwb_is_true_list.append(symbol_name)

    return rwb_is_true_list


