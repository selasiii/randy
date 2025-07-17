# config.py

CONFIG = {
        #main
    "symbol": "BTCUSDm",
    "lot": 0.01,
    "sl_pips": 5000,
    "magic_number": 10001,
    "check_interval": 1,  # seconds to check for new candle
    "timeframe": "M1",
        #anti-martingale
    "enable_antimartingale": True,
    "lot_multiplier": 2,
    "spacing_pips": 10,
    "max_trades": 5,
    
}
