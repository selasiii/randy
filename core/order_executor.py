# core/order_executor.py

import MetaTrader5 as mt5
from utils.mt5_utils import get_point, get_current_tick

def place_order(symbol, order_type, lot, sl_pips, magic):
    tick = get_current_tick(symbol)
    point = get_point(symbol)
    price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
    sl = price - sl_pips * point if order_type == mt5.ORDER_TYPE_BUY else price + sl_pips * point

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": round(sl, 2),
        "deviation": 10,
        "magic": magic,
        "comment": "Randy Init",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Order failed: {result.retcode}")
        return None
    else:
        print(f"✅ {['BUY','SELL'][order_type==mt5.ORDER_TYPE_SELL]} order placed at {price}, SL: {sl}")
        return result.order

def modify_sl(ticket, new_sl):
    position = mt5.positions_get(ticket=ticket)
    if not position:
        print(f"⚠️ No open position found for ticket {ticket}")
        return

    position = position[0]
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": ticket,
        "sl": new_sl,
        "tp": position.tp,
        "symbol": position.symbol,
        "magic": position.magic,
        "comment": "Randy SL Update"
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Failed to modify SL: {result.retcode}")
    else:
        print(f"✅ SL updated for ticket {ticket} → {new_sl}")
