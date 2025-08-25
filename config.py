# config.py
import MetaTrader5 as mt5


CONFIG = {
        #main
    "symbol": "BTCUSDm",
    "lot": 0.01,
    "sl_pips": 4000,
    "magic_number": 10001,
    "check_interval": 2,  # seconds to check for new candle
    "timeframe": mt5.TIMEFRAME_M1,
        #anti-martingale
    "enable_antimartingale": True,
    "lot_multiplier": 2,
    "spacing_pips": 5,
    "max_trades": 9,
        #sl protection
"breakeven_trigger": 500,        # When to set SL to entry
"breakeven_buffer": 200,       # Optional buffer beyond entry
"enable_trailing": True,
"trailing_trigger": 600,         # When to begin trailing
"trailing_distance": 500,          # How much price must move before SL moves again
        #auto close trades  
    "auto_close_before_candle": True,   # toggle auto close before candle
    "close_seconds_before": 10,  # seconds before candle close to close all trades
        "entry_delay_seconds": 5      # wait X seconds after candle open before placing trades

    
}
