# stock_bot.py

import yfinance as yf
import pandas as pd
import ta
import schedule
import time
from datetime import datetime

# === Configuration ===
STOCK_SYMBOL = input("📥 Enter NSE stock symbol (with .NS): ")
INTERVAL = "15m"          # Can be '1d', '15m', '5m', etc.
PERIOD = "7d"             # Can be '1d', '5d', '7d', etc.

RSI_LOWER = 30
RSI_UPPER = 70
SMA_PERIOD = 14

# === Trading Logic ===

def fetch_data():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching data for {STOCK_SYMBOL}...")
    data = yf.download(tickers=STOCK_SYMBOL, period=PERIOD, interval=INTERVAL)
    if data.empty:
        print("⚠️ No data returned. Check symbol or internet connection.")
        return None
    return data

def add_indicators(data):
    data['sma'] = data['Close'].rolling(window=SMA_PERIOD).mean()
    rsi_calc = ta.momentum.RSIIndicator(close=data['Close'].squeeze(), window=SMA_PERIOD)
    data['rsi'] = rsi_calc.rsi()
    return data

def get_signal(rsi_value):
    if rsi_value < RSI_LOWER:
        return "📈 BUY Signal (RSI below 30)"
    elif rsi_value > RSI_UPPER:
        return "📉 SELL Signal (RSI above 70)"
    else:
        return "⏳ HOLD (No action)"

def analyze():
    df = fetch_data()
    if df is None:
        return

    df = add_indicators(df)
    latest = df.iloc[-1]

    # Safely convert to float
    price = float(latest['Close'])
    rsi = float(latest['rsi'])
    sma = float(latest['sma'])
    signal = get_signal(rsi)

    print("\n=== Trading Analysis ===")
    print(f"Date/Time: {datetime.now()}")
    print(f"Price: ₹{price:.2f}")
    print(f"RSI: {rsi:.2f}")
    print(f"SMA: ₹{sma:.2f}")
    print(f"Signal: {signal}")
    print("=========================\n")


# === Scheduler ===

schedule.every(1).hours.do(analyze)

print("🚀 Stock Bot started! Analyzing every hour...\n")
analyze()  # Run once immediately

while True:
    schedule.run_pending()
    time.sleep(1)
