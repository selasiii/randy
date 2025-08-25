# config.py
import MetaTrader5 as mt5

CONFIG = {
    # --- Main ---
    "symbol": "BTCUSDm",
    "lot": 0.01,
    "sl_pips": 4000,
    "magic_number": 10001,
    "check_interval": 2,           # seconds to check for new candle
    "timeframe": mt5.TIMEFRAME_M2,

    # --- Anti-Martingale ---
    "enable_antimartingale": True,
    "lot_multiplier": 2,
    "spacing_pips": 5,
    "max_trades": 9,

    # --- SL Protection (Breakeven & Trailing) ---
    "breakeven_pips": 500,         # price must move this many pips before BE activates
    "breakeven_buffer": 200,       # offset from entry when moving to BE (positive = lock some profit)
    "enable_trailing_stop": True,  # toggle trailing stop
    "trailing_stop_pips": 500,     # distance in pips from current price

    # --- Auto Close Trades ---
    "auto_close_before_candle": True,   # toggle auto close before candle
    "close_seconds_before": 10,         # seconds before candle close to close all trades

    # --- Entry Delay ---
    "entry_delay_seconds": 5            # wait X seconds after candle open before placing trades
}
