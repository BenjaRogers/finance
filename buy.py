
#sample
# api.submit_order(symbol='QDEC',
#                      qty=10,
#                      side='buy',
#                      type='market',
#                      time_in_force='day')

def buy_order(api, ticker_symbol, quantity, type, time_in_force):
    api.submit_order(symbol=ticker_symbol,
                     qty=quantity,
                     type=type,
                     time_in_force=time_in_force)