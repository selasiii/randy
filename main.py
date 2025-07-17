# main.py

import time
import MetaTrader5 as mt5
from config import CONFIG
from utils.mt5_utils import initialize_mt5
from core.candle_handler import get_latest_candle, is_new_candle
from core.order_executor import place_order
from core.trade_manager import (
    check_initial_trade_status,
    trigger_antimartingale,
    manage_antimartingale
)

symbol = CONFIG["symbol"]
lot = CONFIG["lot"]
sl_pips = CONFIG["sl_pips"]
magic = CONFIG["magic_number"]
timeframe = mt5.TIMEFRAME_M1
interval = CONFIG["check_interval"]

# Track tickets
buy_ticket = None
sell_ticket = None

def main():
    print("🚀 Starting Randy Bot...")
    initialize_mt5()
    last_open_time = None

    global buy_ticket, sell_ticket

    while True:
        candle = get_latest_candle(symbol, timeframe)
        if candle is None:
            print("Waiting for candle data...")
            time.sleep(interval)
            continue

        is_new, open_time = is_new_candle(candle['time'], last_open_time)
        if is_new:
            print(f"\n🕒 New candle at {open_time}")
            buy_ticket = place_order(symbol, mt5.ORDER_TYPE_BUY, lot, sl_pips, magic)
            sell_ticket = place_order(symbol, mt5.ORDER_TYPE_SELL, lot, sl_pips, magic)
            last_open_time = open_time

        # Check SL trigger and activate anti-martingale if applicable
        if CONFIG["enable_antimartingale"] and buy_ticket and sell_ticket:
            if not buy_ticket or not sell_ticket:
                print("❌ One or both initial trades failed. Skipping anti-martingale check.")
            else:
                direction = check_initial_trade_status(buy_ticket, sell_ticket)
            if direction:
                trigger_antimartingale(symbol, direction)
                # Reset tickets after determining winner
                buy_ticket = None
                sell_ticket = None

        # Handle ongoing anti-martingale trades
        manage_antimartingale(symbol)

        time.sleep(interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually.")
    finally:
        mt5.shutdown()
