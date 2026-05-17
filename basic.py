from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

api_key='gUwYJAshxoUWwg1YI884pVEO6TmKY6hzeHXS2wv39YVpwAun0h2IkMA96olluF0D'
api_secret='Raxy9dMGl5a4eXW1kpLw9ztHIwOsavXkFaZJpXHSEjmmy3TyudUCfR9eHPAyFS4L'
client = Client()

# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
print(klines)