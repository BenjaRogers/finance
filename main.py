import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd

from Key import api
from Red_White_Blue import get_rwb_list
from Initial_Screen import initial_screen

api = api

for i in range(1):

    #screen stocks initially, to check for rwb throughout day.
    initial_list = initial_screen()

    #get list of potential buy ins based on red white and blue strategy
    buy_list = get_rwb_list()

    # Check against mark minervini conditions

    #determine how big a position to take.





    # Check to sell

    #Initiate buy/sell orders
    print(buy_list)
    i += 1