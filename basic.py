from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

api_key=''
api_secret=''
client = Client()

# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
print(klines)