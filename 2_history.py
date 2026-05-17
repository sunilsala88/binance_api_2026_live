api_key=''
api_secret=''




from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
client = Client(api_key, api_secret)


# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "2 day ago UTC")
print(klines)

import pandas as pd
df=pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')    
print(df.head())
df.to_csv('BTCUSDT_1min_5day.csv', index=False)