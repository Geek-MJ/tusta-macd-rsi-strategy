# Tusta MACD & RSI Strategy Backtester

This Python project fetches historical cryptocurrency data from CoinGecko and runs backtests on MACD and RSI-EMA trading strategies.

---

## Features

- Fetches OHLC data from CoinGecko API  
- Calculates indicators: EMA, MACD, RSI  
- Implements MACD crossover and RSI + EMA strategies  
- Generates trade entries/exits and PnL summary  

---

## Requirements

- Python 3.8+  
- Packages: `requests`, `pandas`, `numpy`, `ta`

---

## Setup Instructions

###1. Clone the repository

```
git clone https://github.com/Geek-MJ/tusta-macd-rsi-strategy.git
cd tusta-macd-rsi-strategy
````

###2. Create and activate a virtual environment (recommended)

On macOS/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

On Windows:

python -m venv venv
.\venv\Scripts\activate


###3. Install dependencies

```
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file, you can create one with:

```
requests
pandas
numpy
ta
```

and then run the install command above.

---

## Running the Script

Run the main Python script:

```
python main.py
```

You will see the fetched data shape, backtest results, and summary printed in the console.

---

## Notes

* Default fetch is for Bitcoin OHLC data for 1 day (can be adjusted in the code).
* Ensure you have a stable internet connection to fetch data from CoinGecko.

---

## Contributing

Feel free to submit issues or pull requests to improve this project.
