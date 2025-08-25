import MetaTrader5 as mt5
from datetime import datetime

def time_left_in_candle(timeframe):
    """
    Returns how many seconds are left before the current candle closes.
    """
    now = datetime.now()

    # Map MT5 timeframes to their duration in seconds
    tf_map = {
        mt5.TIMEFRAME_M1: 60,
        mt5.TIMEFRAME_M5: 300,
        mt5.TIMEFRAME_M15: 900,
        mt5.TIMEFRAME_M30: 1800,
        mt5.TIMEFRAME_H1: 3600,
    }

    tf_seconds = tf_map.get(timeframe, 60)

    # Normalize candle start (to nearest lower multiple of timeframe)
    elapsed = (now.minute * 60 + now.second) % tf_seconds
    return tf_seconds - elapsed
