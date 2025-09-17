# main.py

import MetaTrader5 as mt5
from core.trade_manager import place_zone_orders
from config import CONFIG


def main():
    symbol = input("Enter symbol (e.g. XAUUSD): ").strip()
    direction = input("Direction (buy/sell): ").strip().lower()

    lower_limit = float(input("Enter lower price limit: "))
    upper_limit = float(input("Enter upper price limit: "))
    spacing_pips = int(input("Enter spacing in pips: "))

    sl_price = float(input("Enter Stop Loss price: "))
    tp_price = float(input("Enter Take Profit price: "))
    base_lot = float(input("Enter base lot size: "))

    antimartingale_enabled = input("Enable Anti-Martingale lot sizing? (y/n): ").strip().lower() == "y"
    antimartingale_mode = "incremental"
    increment_step = 1.0
    exponential_factor = 2.0

    if antimartingale_enabled:
        antimartingale_mode = input("Mode (incremental/exponential): ").strip().lower()
        if antimartingale_mode == "incremental":
            increment_step = float(input("Enter increment step (e.g. 0.5): "))
        elif antimartingale_mode == "exponential":
            exponential_factor = float(input("Enter exponential factor (e.g. 2.0): "))

    tickets = place_zone_orders(
        symbol=symbol,
        direction=direction,
        lower_price=lower_limit,
        upper_price=upper_limit,
        spacing_pips=spacing_pips,
        sl_price=sl_price,
        tp_price=tp_price,
        base_lot=base_lot,
        antimartingale_enabled=antimartingale_enabled,
        antimartingale_mode=antimartingale_mode,
        increment_step=increment_step,
        exponential_factor=exponential_factor,
        magic=CONFIG["magic"],
    )

    if tickets:
        print(f"✅ Placed {len(tickets)} pending orders for {symbol}")
    else:
        print("❌ No orders placed.")


if __name__ == "__main__":
    if not mt5.initialize():
        print("❌ initialize() failed, error:", mt5.last_error())
        quit()
    try:
        main()
    finally:
        mt5.shutdown()
