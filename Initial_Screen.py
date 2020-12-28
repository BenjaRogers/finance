import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import csv


#initialize yfinance
yf.pdr_override()

##### establish date time parameters.
# start_year = 2020
# start_month = 1
# start_day = 1
now = dt.datetime.now()
start = dt.datetime(now.year - 1, now.month, now.day)

#retrieve stock symbols from excel spreadsheet
stock_list = pd.read_csv("bats_symbols.csv")

def initial_screen():

    export_df = pd.DataFrame(columns=['Stock', "Close Price", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])
    potential_positions_list = []
    for stock in stock_list.index:
        stock_name = str(stock_list["Name"][stock])
        #rs_rating = stock_list["RS Rating"][stock]
        try:
            df = pdr.get_data_yahoo(stock_name, start, now)
            DAYS = [50, 150, 200]
            for x in DAYS:
                sma = x
                df["sma_" + str(sma)] = round(df.iloc[:,4].rolling(window=sma).mean(), 2)

            simp_mov_avg_50 = df["sma_50"][-1]
            simp_mov_avg_150 = df["sma_150"][-1]
            simp_mov_avg_200 = df["sma_200"][-1]
            close_price = df["Adj Close"][-1]
            low_price = min(df["Adj Close"][:])
            max_price = max(df["Adj Close"][:])

            month_simp_move_200 = df["sma_200"][-20]

            print("Checking " + stock_name + ".....")
            print(
                f"The simple moving average for 50 , 150 and 200 days is {simp_mov_avg_50}   {simp_mov_avg_150}    {simp_mov_avg_200}")
            print(f"the closing price is {close_price} \t the low price is {low_price} and the max is {max_price}")
            #print("The RS is:  ", rs_rating)

            # Check Mark Minervini's conditions for screening stocks
            # 1) The current price of the stock must be above 150 & 200 day simple moving averages
            if simp_mov_avg_150 < close_price > simp_mov_avg_200:
                condition_1 = True
            else:
                condition_1 = False
                print("Condition 1 was not met")
                continue

            # 2) The 150 day simple moving average must be above the 200 day simple moving average
            if simp_mov_avg_150 > simp_mov_avg_200:
                condition_2 = True
            else:
                condition_2 = False
                print("Condition 2 was not met")
                continue

            # 3) The 200 day simple moving average must be trending up for at least 1 month
            if close_price >= month_simp_move_200:
                condition_3 = True
            else:
                condition_3 = False
                print("Condition 3 was not met")
                continue

            # 4) The 50 day simple moving  average must be above both 150 and 200 simple moving average
            if simp_mov_avg_50 > simp_mov_avg_150 and simp_mov_avg_50 > simp_mov_avg_200:
                condition_4 = True
            else:
                condition_4 = False
                print("Condition 4 was not met")
                continue

            # 5) The current price must be trading above 50 day simple moving average
            if close_price > simp_mov_avg_50:
                condition_5 = True
            else:
                condition_5 = False
                print("Condition 5 was not met")
                continue

            # 6) The current price must be >= 30% above 52 week low
            if close_price >= low_price * 1.3:
                condition_6 = True
            else:
                condition_6 = False
                print("Condition 6 was not met")
                continue

            # 7) The current price must be within 25% of the 52 weeks high
            if close_price <= max_price * 1.25 and close_price >= max_price * 0.75:
                condition_7 = True
            else:
                condition_7 = False
                print("Condition 7 was not met")
                continue

            # 8) The RS > 70
            # if rs_rating > 70:
            #     condition_8 = True
            # else:
            #     condition_8 = False
            #     continue
            if condition_1 == True and condition_2 == True and condition_3 == True and condition_4 == True and\
                    condition_5 == True and condition_6 == True and condition_7 == True:
                potential_positions_list.append(stock_name)
        except:

            print("unavailable")
    return potential_positions_list
print(initial_screen())