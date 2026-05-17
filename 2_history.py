api_key=''
api_secret=''




from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
client = Client(api_key, api_secret)


# Fetch current quote/ticker price for a single symbol
def get_single_quote(symbol):
    """Fetch current price for a single symbol"""
    ticker = client.get_symbol_info(symbol)
    price = client.get_symbol_ticker(symbol=symbol)
    print(f"{symbol}: ${price['price']}")
    return price

# Fetch current prices for multiple symbols
def get_multiple_quotes(symbols):
    """Fetch current prices for multiple symbols"""
    prices = client.get_all_tickers()
    filtered = [p for p in prices if p['symbol'] in symbols]
    for quote in filtered:
        print(f"{quote['symbol']}: ${quote['price']}")
    return filtered

# Fetch 24-hour ticker statistics
def get_24h_ticker(symbol):
    """Fetch 24-hour statistics for a symbol"""
    ticker_24h = client.get_ticker(symbol=symbol)
    print(f"\n24h Stats for {symbol}:")
    print(f"  Last Price: ${ticker_24h['lastPrice']}")
    print(f"  24h High: ${ticker_24h['highPrice']}")
    print(f"  24h Low: ${ticker_24h['lowPrice']}")
    print(f"  24h Volume: {ticker_24h['volume']} {symbol.replace('USDT', '')}")
    print(f"  24h Change: {ticker_24h['priceChangePercent']}%")
    return ticker_24h

# Example usage:
quote = get_single_quote("BTCUSDT")
print(quote)
# quotes = get_multiple_quotes(["BTCUSDT", "ETHUSDT", "BNBUSDT"])
# stats = get_24h_ticker("BTCUSDT")


