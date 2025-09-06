import MetaTrader5 as mt5
from datetime import datetime, timedelta


def time_left_in_candle(timeframe):
    """
    Returns how many seconds are left before the current candle closes.
    Uses UTC time for consistency.
    """
    now = datetime.utcnow()
    ts = now.timestamp()

    # Map MT5 timeframes to duration in seconds (added M2)
    tf_map_seconds = {
        mt5.TIMEFRAME_M1: 60,
        mt5.TIMEFRAME_M2: 120,
        mt5.TIMEFRAME_M5: 300,
        mt5.TIMEFRAME_M15: 900,
        mt5.TIMEFRAME_M30: 1800,
        mt5.TIMEFRAME_H1: 3600,
        mt5.TIMEFRAME_H4: 3600 * 4,
        mt5.TIMEFRAME_D1: 3600 * 24,
    }

    tf_seconds = tf_map_seconds.get(timeframe, 60)
    elapsed = ts % tf_seconds
    remaining = tf_seconds - elapsed
    return int(remaining)


def get_next_candle_time(symbol: str, timeframe: int) -> datetime:
    """
    Compute the UTC datetime of the next candle open for the given timeframe.
    This computes locally (no reliance on MT5 rates) using epoch modulo arithmetic.
    """
    now = datetime.utcnow()
    ts = now.timestamp()

    tf_map_seconds = {
        mt5.TIMEFRAME_M1: 60,
        mt5.TIMEFRAME_M2: 120,
        mt5.TIMEFRAME_M5: 300,
        mt5.TIMEFRAME_M15: 900,
        mt5.TIMEFRAME_M30: 1800,
        mt5.TIMEFRAME_H1: 3600,
        mt5.TIMEFRAME_H4: 3600 * 4,
        mt5.TIMEFRAME_D1: 3600 * 24,
    }

    tf_seconds = tf_map_seconds.get(timeframe)
    if tf_seconds is None:
        raise ValueError(f"Unsupported timeframe: {timeframe}")

    elapsed = ts % tf_seconds
    secs_to_next = tf_seconds - elapsed
    next_dt = now + timedelta(seconds=secs_to_next)
    return next_dt
