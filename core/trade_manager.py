from datetime import datetime, timedelta
import MetaTrader5 as mt5
from utils.mt5_utils import get_point, get_current_tick
from core.order_executor import place_order
from config import CONFIG

antimartingale_active = False
antimartingale_count = 0
last_direction = None  # 'buy' or 'sell'
open_positions = []  # To track all antimartingale trades (tickets)

def check_initial_trade_status(buy_ticket, sell_ticket):
    print(f"🔍 Checking SL outcome for Buy: {buy_ticket}, Sell: {sell_ticket}")
    now = datetime.now()
    history = mt5.history_deals_get(now - timedelta(minutes=10), now)

    if history is None or len(history) == 0:
        print("⚠️ No historical deals found.")
        return None

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

    if buy_closed_sl and not sell_closed_sl:
        return "sell"
    elif sell_closed_sl and not buy_closed_sl:
        return "buy"
    else:
        print("❓ Both trades closed or unclear outcome.")
        return None

def trigger_antimartingale(symbol, direction):
    global antimartingale_active, antimartingale_count, last_direction, open_positions

    if antimartingale_active:
        return

    antimartingale_active = True
    antimartingale_count = 0
    last_direction = direction
    open_positions = []
    print(f"🚀 Starting anti-martingale in direction: {direction.upper()}")

def manage_antimartingale(symbol):
    global antimartingale_count, antimartingale_active, open_positions

    if not antimartingale_active:
        return

    # Place new trade if limit not hit
    if antimartingale_count < CONFIG["max_trades"]:
        lot = CONFIG["lot"] * (CONFIG["lot_multiplier"] ** antimartingale_count)
        spacing_pips = CONFIG["spacing_pips"]
        point = get_point(symbol)
        current_price = get_current_tick(symbol).ask if last_direction == "buy" else get_current_tick(symbol).bid

        entry_price = current_price + (spacing_pips * point * antimartingale_count) if last_direction == "buy" \
            else current_price - (spacing_pips * point * antimartingale_count)

        order_type = mt5.ORDER_TYPE_BUY if last_direction == "buy" else mt5.ORDER_TYPE_SELL
        print(f"📈 Placing anti-martingale #{antimartingale_count + 1}: {last_direction.upper()} @ {entry_price}")
        ticket = place_order(symbol, order_type, lot, CONFIG["sl_pips"], CONFIG["magic_number"])
        if ticket:
            open_positions.append(ticket)
            antimartingale_count += 1
    else:
        print("✅ Anti-martingale sequence complete.")
        antimartingale_active = False

    # Breakeven and trailing logic for all active positions
    for ticket in open_positions:
        position = mt5.positions_get(ticket=ticket)
        if position and len(position) > 0:
            pos = position[0]
            current_price = get_current_tick(symbol).ask if pos.type == mt5.ORDER_TYPE_BUY else get_current_tick(symbol).bid
            profit_pips = (current_price - pos.price_open) / get_point(symbol) if pos.type == mt5.ORDER_TYPE_BUY else (pos.price_open - current_price) / get_point(symbol)

            # --- Breakeven logic ---
            if profit_pips >= CONFIG["breakeven_pips"]:
                new_sl = pos.price_open + CONFIG["breakeven_buffer"] * get_point(symbol) if pos.type == mt5.ORDER_TYPE_BUY \
                         else pos.price_open - CONFIG["breakeven_buffer"] * get_point(symbol)

                if (pos.sl == 0) or (pos.type == mt5.ORDER_TYPE_BUY and new_sl > pos.sl) or (pos.type == mt5.ORDER_TYPE_SELL and new_sl < pos.sl):
                    modify_sl(ticket, new_sl)

            # --- Trailing stop logic ---
            if CONFIG["enable_trailing_stop"] and profit_pips > CONFIG["breakeven_pips"]:
                trailing_sl = current_price - CONFIG["trailing_stop_pips"] * get_point(symbol) if pos.type == mt5.ORDER_TYPE_BUY \
                              else current_price + CONFIG["trailing_stop_pips"] * get_point(symbol)

                if (pos.type == mt5.ORDER_TYPE_BUY and trailing_sl > pos.sl) or (pos.type == mt5.ORDER_TYPE_SELL and trailing_sl < pos.sl):
                    modify_sl(ticket, trailing_sl)

def modify_sl(ticket, new_sl):
    position = mt5.positions_get(ticket=ticket)
    if position is None or len(position) == 0:
        return

    pos = position[0]
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": ticket,
        "sl": round(new_sl, 5),
        "tp": pos.tp,
        "symbol": pos.symbol,
        "magic": pos.magic,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"⚠️ SL modification failed for ticket {ticket}: {result.retcode}")
    else:
        print(f"🔁 SL modified for ticket {ticket}: New SL = {new_sl}")
