# utils/mt5_utils.py

import MetaTrader5 as mt5

def initialize_mt5():
    if not mt5.initialize():
        raise RuntimeError("❌ MT5 initialization failed.")
    return True

def get_point(symbol):
    info = mt5.symbol_info(symbol)
    if info is None:
        raise ValueError(f"Symbol '{symbol}' not found.")
    return info.point

def get_current_tick(symbol):
    return mt5.symbol_info_tick(symbol)
