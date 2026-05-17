"""
Real-time BTCUSDT data fetch using Binance WebSocket
Using ThreadedWebsocketManager for real-time streaming data
Documentation: https://python-binance.readthedocs.io/en/latest/websockets.html
"""
import os
from datetime import datetime
from binance import ThreadedWebsocketManager

def message_handler(msg):
    """
    Handle incoming WebSocket messages
    """
    if msg.get('e') == 'error':
        print(f"WebSocket error: {msg.get('type')} - {msg.get('m')}")
    else:
        try:
            # For kline data
            if msg.get('e') == 'kline':
                event_time = datetime.fromtimestamp(msg['E'] / 1000)
                symbol = msg['s']
                kline = msg['k']
                
                open_price = kline['o']
                high_price = kline['h']
                low_price = kline['l']
                close_price = kline['c']
                volume = kline['v']
                is_closed = kline['x']  # Is this kline closed?
                
                status = "CLOSED" if is_closed else "ACTIVE"
                
                print(f"[{event_time}] {symbol} {status}")
                print(f"  Open: {open_price}, High: {high_price}, Low: {low_price}, Close: {close_price}")
                print(f"  Volume: {volume}\n")
            
            # For trade data
            elif msg.get('e') == 'trade':
                event_time = datetime.fromtimestamp(msg['E'] / 1000)
                symbol = msg['s']
                price = msg['p']
                quantity = msg['q']
                buyer_maker = msg['m']  # True if buyer is maker
                
                side = "SELL" if buyer_maker else "BUY"
                print(f"[{event_time}] {symbol} TRADE: {side} {quantity} @ {price}\n")
            
            # For ticker data
            elif msg.get('e') == '24hrTicker':
                symbol = msg['s']
                price_change = msg['p']
                price_change_percent = msg['P']
                last_price = msg['c']
                
                print(f"[{symbol}] Price: {last_price}, Change: {price_change} ({price_change_percent}%)\n")
                
        except Exception as e:
            print(f"Error processing message: {e}")
            print(f"Message: {msg}\n")


def start_kline_stream(twm, symbol="BTCUSDT", interval="1m"):
    """
    Start kline (candlestick) stream
    Intervals: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    """
    print(f"Starting {interval} kline stream for {symbol}...")
    return twm.start_kline_socket(callback=message_handler, symbol=symbol, interval=interval)


def start_trade_stream(twm, symbol="BTCUSDT"):
    """
    Start individual trade stream
    """
    print(f"Starting trade stream for {symbol}...")
    return twm.start_trade_socket(callback=message_handler, symbol=symbol)


def start_ticker_stream(twm, symbol="BTCUSDT"):
    """
    Start 24hr ticker stream
    """
    print(f"Starting 24hr ticker stream for {symbol}...")
    return twm.start_symbol_ticker_socket(callback=message_handler, symbol=symbol)


if __name__ == "__main__":
    print("=" * 60)
    print("Binance Real-time BTCUSDT Data WebSocket Stream")
    print("=" * 60)
    print("\nNote: If you get SSL certificate errors, you may need to:")
    print("  1. Update your SSL certificates: /Applications/Python/Install\\ Certificates.command")
    print("  2. Or upgrade certifi: pip install --upgrade certifi\n")
    
    try:
        # Create ThreadedWebsocketManager instance
        # No special SSL parameters needed - use defaults
        twm = ThreadedWebsocketManager()
        
        # Start the manager (required before starting any sockets)
        twm.start()
        
        # Start streaming data - choose one or more:
        
        # Option 1: Kline (1-minute candlestick) data
        kline_stream_name = start_kline_stream(twm, symbol="BTCUSDT", interval="1m")
        
        # Option 2: Individual trades
        # trade_stream_name = start_trade_stream(twm, symbol="BTCUSDT")
        
        # Option 3: 24hr ticker
        # ticker_stream_name = start_ticker_stream(twm, symbol="BTCUSDT")
        
        print("\nStreaming data... (Press Ctrl+C to stop)\n")
        
        # Keep the manager running
        twm.join()
        
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        if 'twm' in locals():
            twm.stop()
        print("WebSocket streams closed")
    except Exception as e:
        print(f"Error: {e}")
        if 'twm' in locals():
            twm.stop()
