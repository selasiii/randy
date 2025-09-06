# main.py

import MetaTrader5 as mt5
from core.trade_manager import place_zone_orders
from config import CONFIG

def main():
    # Initialize MT5
    if not mt5.initialize():
        print("❌ MT5 initialization failed")
        return

    print("\n=== Randy Phase 5: Zone Orders ===\n")

    # Collect console inputs
    symbol = input(f"Symbol (default={CONFIG['symbol']}): ") or CONFIG["symbol"]

    direction = input("Direction (buy/sell): ").strip().lower()
    while direction not in ["buy", "sell"]:
        direction = input("Invalid. Enter direction (buy/sell): ").strip().lower()

    try:
        lower_limit = float(input("Lower price of zone: "))
        upper_limit = float(input("Upper price of zone: "))
    except ValueError:
        print("❌ Invalid price inputs.")
        mt5.shutdown()
        return

    try:
        spacing_pips = float(input("Spacing between orders (pips): "))
    except ValueError:
        print("❌ Invalid spacing.")
        mt5.shutdown()
        return

    try:
        sl_price = float(input("Stop Loss price: "))
        tp_price = float(input("Take Profit price: "))
    except ValueError:
        print("❌ Invalid SL/TP.")
        mt5.shutdown()
        return

    try:
        lot = float(input(f"Lot size (default={CONFIG['lot']}): ") or CONFIG["lot"])
    except ValueError:
        print("❌ Invalid lot size.")
        mt5.shutdown()
        return

    # Place zone orders
    place_zone_orders(
        symbol=symbol,
        direction=direction,
        lower=lower_limit,
        upper=upper_limit,
        spacing_pips=spacing_pips,
        sl_price=sl_price,
        tp_price=tp_price,
        lot=lot,
        magic=CONFIG["magic"],
    )

    mt5.shutdown()


if __name__ == "__main__":
    main()
