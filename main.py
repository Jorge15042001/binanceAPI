import time
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from keys import api_key, api_secret

import json
import pandas as pd
import plotly.express as px

client = Client(api_key, api_secret)

#  coins = client.get_all_tickers()

#  coins = client.get_ticker()
#  for coin in coins:
#      print(coin)

#  count = 0
#  for coin in coins:
#      if coin["symbol"].endswith("BUSD"):
#          print (coin)
#          count +=1

#  klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
#  print(klines)

depth = client.get_order_book(symbol='SOLBUSD')

bids = depth["bids"].copy()
bids.sort(key=lambda x:float(x[0]))
bids_price = list(map(lambda x:float(x[0]),bids))
bids_quantity = list(map(lambda x:float(x[1]),bids))
for i in range (-2,-len(bids_quantity)-1,-1):
    bids_quantity[i]+=bids_quantity[i+1]

asks = depth["asks"].copy()
asks.sort(key=lambda x:float(x[0]))
asks_price = list(map(lambda x:float(x[0]),asks))
asks_quantity = list(map(lambda x:float(x[1]),asks))
for i in range(1,len(asks_quantity)):
    asks_quantity[i]+=asks_quantity[i-1]

prices = bids_price+asks_price
asksQuantity = [0]*len(bids_quantity)+asks_quantity
bidsQuantity = bids_quantity + [0]*len(asks_quantity)

df = pd.DataFrame({
    "price":prices,
    "asks":asksQuantity,
    "bids":bidsQuantity
    })



fig = px.area(df,x="price",y=["asks","bids"])
fig2 = px.line(df,x="price",y=["asks","bids"])
fig2.show()
fig.show()


#  for kline in client.get_historical_klines_generator("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
#      print(kline)

def main():

    #  symbol = 'DOTBUSD'
    #
    #  twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    #  # start is required to initialise its internal loop
    #  twm.start()
    #
    #  def handle_socket_message(msg):
    #      print(f"message type: {msg['e']}")
    #      print(msg)
    #
    #  twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
    #
    #  # multiple sockets can be started
    #  #  twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)
    #
    #  # or a multiplex socket can be started like this
    #  # see Binance docs for stream names
    #  #  streams = ['bnbbtc@miniTicker', 'bnbbtc@bookTicker']
    #  #  twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)
    #  twm.join()
    #
    #
    pass
if __name__ == "__main__":
   main()

