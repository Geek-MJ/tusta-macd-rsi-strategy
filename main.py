import requests
import pandas as pd
import numpy as np
from ta.trend import MACD, EMAIndicator
from ta.momentum import RSIIndicator


def fetch_coingecko_data(symbol_id='bitcoin', days='1'):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol_id}/ohlc?vs_currency=usd&days={days}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("Error fetching data from CoinGecko:", e)
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    df['volume'] = np.nan
    return df


def add_indicators(df):
    df['ema_12'] = EMAIndicator(close=df['close'], window=12).ema_indicator()
    df['ema_26'] = EMAIndicator(close=df['close'], window=26).ema_indicator()
    df['macd_line'] = MACD(close=df['close']).macd()
    df['macd_ema'] = EMAIndicator(close=df['macd_line'], window=9).ema_indicator()
    df['ema_21'] = EMAIndicator(close=df['close'], window=21).ema_indicator()
    df['rsi'] = RSIIndicator(close=df['close']).rsi()

    df.dropna(subset=['ema_12', 'ema_26', 'macd_line', 'macd_ema', 'ema_21', 'rsi'], inplace=True)
    return df


def macd_strategy(df):
    entries, exits = [], []  
    position = False

    for i in range(1, len(df)):
        if not position and df['macd_line'].iloc[i] > df['macd_ema'].iloc[i] and df['macd_line'].iloc[i - 1] <= \
                df['macd_ema'].iloc[i - 1]:
            entries.append((df.index[i], df['close'].iloc[i]))
            position = True
        elif position and df['macd_line'].iloc[i] < df['macd_ema'].iloc[i] and df['macd_line'].iloc[i - 1] >= \
                df['macd_ema'].iloc[i - 1]:
            exits.append((df.index[i], df['close'].iloc[i]))
            position = False

    return entries, exits


def rsi_ema_strategy(df):
    entries, exits = [], []   
    position = False

    for i in range(1, len(df)):
        if not position and df['rsi'].iloc[i] > 30 and df['close'].iloc[i] > df['ema_21'].iloc[i] and \
                (df['rsi'].iloc[i - 1] <= 30 or df['close'].iloc[i - 1] <= df['ema_21'].iloc[i - 1]):
            entries.append((df.index[i], df['close'].iloc[i]))
            position = True
        elif position and (df['rsi'].iloc[i] < 70 or df['close'].iloc[i] < df['ema_21'].iloc[i]):
            exits.append((df.index[i], df['close'].iloc[i]))
            position = False

    return entries, exits


def backtest(entries, exits, strategy_name):
    trades = []
    min_len = min(len(entries), len(exits))

    for i in range(min_len):
        entry = entries[i]
        exit = exits[i]
        pnl = exit[1] - entry[1]
        status = 'Win' if pnl > 0 else 'Loss'
        trades.append({
            'Entry Time': entry[0],
            'Entry Price': entry[1],
            'Exit Time': exit[0],
            'Exit Price': exit[1],
            'Strategy': strategy_name,
            'PnL': pnl,
            'Status': status
        })

    return pd.DataFrame(trades) if trades else pd.DataFrame(
        columns=['Entry Time', 'Entry Price', 'Exit Time', 'Exit Price', 'Strategy', 'PnL', 'Status'])


def main():
    df = fetch_coingecko_data()  # default = 1 day bitcoin OHLC
    print("Fetched data shape:", df.shape)

    if df.empty:
        print("Failed to fetch data.")
        return

    df = add_indicators(df)
    print("Data after adding indicators:", df.shape)

    if df.empty:
        print("Data is empty after indicator calculation.")
        return

    macd_entries, macd_exits = macd_strategy(df)
    rsi_entries, rsi_exits = rsi_ema_strategy(df)

    macd_trades = backtest(macd_entries, macd_exits, "MACD Strategy")
    rsi_trades = backtest(rsi_entries, rsi_exits, "RSI-EMA Strategy")

    all_trades = pd.concat([macd_trades, rsi_trades]).sort_values(by='Entry Time').reset_index(drop=True)

    print("\n🔹 Backtest Results 🔹")
    print(all_trades)

    print("\nSummary:")
    print("Total Trades:", len(all_trades))
    print("Winning Trades:", len(all_trades[all_trades['Status'] == 'Win']))
    print("Losing Trades:", len(all_trades[all_trades['Status'] == 'Loss']))
    print("Net PnL:", all_trades['PnL'].sum())


if __name__ == "__main__":
    main()
