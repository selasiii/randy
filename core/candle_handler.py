# core/candle_handler.py

import MetaTrader5 as mt5
from datetime import datetime
import pytz

timezone = pytz.timezone("Etc/UTC")

def get_latest_candle(symbol, timeframe):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 2)
    if rates is None or len(rates) < 2:
        return None
    return rates[-1]

def is_new_candle(latest_candle_time, previous_time):
    open_time = datetime.fromtimestamp(latest_candle_time, tz=timezone)
    return open_time != previous_time, open_time
