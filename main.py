# main.py

import time
import MetaTrader5 as mt5
from config import CONFIG
from utils.mt5_utils import initialize_mt5
from utils.time_utils import time_left_in_candle
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
timeframe = CONFIG["timeframe"]
interval = CONFIG["check_interval"]

# Track tickets
buy_ticket = None
sell_ticket = None

def close_all_trades():
    """
    Closes all open trades for the current symbol.
    """
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        return

    for pos in positions:
        order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(pos.symbol).bid if order_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(pos.symbol).ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": order_type,
            "position": pos.ticket,
            "price": price,
            "deviation": 20,
            "magic": CONFIG["magic_number"],
            "comment": "Auto-close before candle end"
        }
        result = mt5.order_send(request)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"🛑 Closed position {pos.ticket} ({pos.symbol}, {pos.volume} lots)")
        else:
            print(f"⚠️ Failed to close position {pos.ticket}. Retcode: {result.retcode}")

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

        # ✅ Auto-close trades before candle end
        if CONFIG.get("auto_close_before_candle", False):
            seconds_left = time_left_in_candle(timeframe)
            if seconds_left <= CONFIG.get("close_seconds_before", 10):
                close_all_trades()

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
