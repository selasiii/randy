#utils/pip_utils.py

import MetaTrader5 as mt5

def get_symbol_info(symbol):
    """Fetch symbol info from MT5."""
    info = mt5.symbol_info(symbol)
    if not info:
        raise RuntimeError(f"Symbol {symbol} not found in MT5.")
    return info

def pip_size(symbol):
    """
    Returns the pip size for a symbol.
    Normalizes pip definition across different broker digits.
    """
    info = get_symbol_info(symbol)

    # 5-digit FX pairs (EURUSD = 1.12345 → pip = 0.0001)
    if info.digits == 5:
        return 0.0001
    # 3-digit FX pairs (USDJPY = 123.456 → pip = 0.01)
    elif info.digits == 3:
        return 0.01
    # Metals like XAUUSD (2 digits → pip = 0.01)
    elif info.digits == 2:
        return 0.01
    # Cryptos or indices may have 1 digit (BTCUSDm = 26850.5 → pip = 0.1)
    elif info.digits == 1:
        return 0.1
    # 4-digit FX pairs (rare brokers → pip = 0.0001)
    elif info.digits == 4:
        return 0.0001
    else:
        # fallback: use broker point size
        return info.point

def pips_to_price(symbol, pips):
    """Convert pips to price distance."""
    return pips * pip_size(symbol)

def price_to_pips(symbol, price_diff):
    """Convert raw price difference into pips."""
    return price_diff / pip_size(symbol)
