# trade_manager.py

from datetime import datetime, timedelta
import MetaTrader5 as mt5
from utils.mt5_utils import get_point, get_current_tick
from core.order_executor import place_order
from config import CONFIG

antimartingale_active = False
antimartingale_count = 0
last_direction = None  # 'buy' or 'sell'


def check_initial_trade_status(buy_ticket, sell_ticket):
    print(f"🔍 Checking SL outcome for Buy: {buy_ticket}, Sell: {sell_ticket}")

    # Step 1: Get all deals from the last few minutes
    now = datetime.now()
    history = mt5.history_deals_get(now - timedelta(minutes=10), now)

    if history is None or len(history) == 0:
        print("⚠️ No historical deals found.")
        return None

    # Step 2: Track SL result by matching tickets and checking SL closures
    buy_closed_sl = False
    sell_closed_sl = False

    for deal in history:
        if deal.position_id == buy_ticket and deal.type == mt5.DEAL_TYPE_SELL:
            if deal.entry == mt5.DEAL_ENTRY_OUT and deal.reason == mt5.DEAL_REASON_SL:
                buy_closed_sl = True
        if deal.position_id == sell_ticket and deal.type == mt5.DEAL_TYPE_BUY:
            if deal.entry == mt5.DEAL_ENTRY_OUT and deal.reason == mt5.DEAL_REASON_SL:
                sell_closed_sl = True

    print(f"🧾 Buy SL: {buy_closed_sl}, Sell SL: {sell_closed_sl}")

    # Step 3: Infer winner based on which one got stopped out
    if buy_closed_sl and not sell_closed_sl:
        return "sell"
    elif sell_closed_sl and not buy_closed_sl:
        return "buy"
    else:
        print("❓ Both trades closed or unclear outcome.")
        return None


def trigger_antimartingale(symbol, direction):
    global antimartingale_active, antimartingale_count, last_direction

    if antimartingale_active:
        return

    antimartingale_active = True
    antimartingale_count = 0
    last_direction = direction
    print(f"🚀 Starting anti-martingale in direction: {direction.upper()}")

def manage_antimartingale(symbol):
    global antimartingale_count, antimartingale_active

    if not antimartingale_active:
        return

    if antimartingale_count >= CONFIG["max_trades"]:
        print("✅ Anti-martingale sequence complete.")
        antimartingale_active = False
        return

    lot = CONFIG["lot"] * (CONFIG["lot_multiplier"] ** antimartingale_count)
    spacing_pips = CONFIG["spacing_pips"]
    point = get_point(symbol)
    current_price = get_current_tick(symbol).ask if last_direction == "buy" else get_current_tick(symbol).bid

    entry_price = current_price + (spacing_pips * point * antimartingale_count) if last_direction == "buy" \
        else current_price - (spacing_pips * point * antimartingale_count)

    order_type = mt5.ORDER_TYPE_BUY if last_direction == "buy" else mt5.ORDER_TYPE_SELL
    print(f"📈 Placing anti-martingale #{antimartingale_count + 1}: {last_direction.upper()} @ {entry_price}")
    
    place_order(symbol, order_type, lot, CONFIG["sl_pips"], CONFIG["magic_number"])
    antimartingale_count += 1
