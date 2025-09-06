# order_executor.py

import MetaTrader5 as mt5
import uuid
from datetime import datetime


def _round_price(symbol: str, price: float) -> float:
    """Round price to correct digits for the symbol."""
    info = mt5.symbol_info(symbol)
    if not info:
        raise RuntimeError(f"Symbol info not found for {symbol}")
    return round(price, info.digits)


def place_order(symbol, order_type, lot, sl_price, tp_price, magic):
    """
    Place a market order with absolute SL/TP prices.
    Returns the position ticket if successful, None otherwise.
    """
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print("❌ No tick data available.")
        return None

    price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
    sl = _round_price(symbol, sl_price) if sl_price else 0.0
    tp = _round_price(symbol, tp_price) if tp_price else 0.0

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": _round_price(symbol, price),
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": magic,
        "comment": "Randy Market",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Market order failed: retcode={getattr(result, 'retcode', None)}")
        return None

    pos_ticket = result.order if result.order else None
    print(f"✅ Market order filled @ {request['price']} | SL={sl}, TP={tp} | ticket={pos_ticket}")
    return pos_ticket


def place_pending_order(symbol, order_type, lot, entry_price, sl_price, tp_price, magic, expiration=None):
    """
    Place a pending STOP/LIMIT order with absolute SL/TP.
    Returns the order ticket if successful, None otherwise.
    """
    uid = str(uuid.uuid4())[:8]  # short UID for tracking
    entry_price = _round_price(symbol, entry_price)
    sl = _round_price(symbol, sl_price) if sl_price else 0.0
    tp = _round_price(symbol, tp_price) if tp_price else 0.0

    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": entry_price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": magic,
        "comment": f"Randy Pending {uid}",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    if expiration:
        request["type_time"] = mt5.ORDER_TIME_SPECIFIED
        request["expiration"] = expiration

    result = mt5.order_send(request)
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Pending order failed at {entry_price} | retcode={getattr(result, 'retcode', None)}")
        return None

    order_ticket = result.order if result.order else None
    print(f"✅ Pending order placed @ {entry_price} | SL={sl}, TP={tp} | ticket={order_ticket}, uid={uid}")
    return order_ticket


def cancel_pending_order(order_ticket: int):
    """Cancel a pending order by ticket."""
    if not order_ticket:
        return False

    request = {
        "action": mt5.TRADE_ACTION_REMOVE,
        "order": order_ticket,
    }

    result = mt5.order_send(request)
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"⚠️ Failed to cancel pending order {order_ticket}")
        return False

    print(f"🗑️ Pending order {order_ticket} cancelled successfully.")
    return True


def modify_sl(position_ticket: int, new_sl: float):
    """Modify SL for an open position."""
    pos = mt5.positions_get(ticket=position_ticket)
    if not pos:
        print(f"⚠️ No open position found for ticket {position_ticket}")
        return False

    pos = pos[0]
    rounded_sl = _round_price(pos.symbol, new_sl)

    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": position_ticket,
        "sl": rounded_sl,
        "tp": pos.tp,
        "symbol": pos.symbol,
        "magic": pos.magic,
        "comment": "Randy SL Update",
    }

    result = mt5.order_send(request)
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Failed to modify SL for ticket {position_ticket}")
        return False

    print(f"✅ SL updated for ticket {position_ticket} → {rounded_sl}")
    return True


def close_all_positions(symbol, magic):
    """Close all positions for a given symbol and magic number."""
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print("⚠️ No positions to close.")
        return

    for pos in positions:
        if pos.magic != magic:
            continue

        order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": pos.volume,
            "type": order_type,
            "position": pos.ticket,
            "price": _round_price(symbol, price),
            "magic": magic,
            "comment": "Randy Close All",
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"✅ Closed position {pos.ticket}")
        else:
            print(f"❌ Failed to close position {pos.ticket}")


def cancel_all_pending(symbol, magic):
    """Cancel all pending orders for a symbol and magic number."""
    orders = mt5.orders_get(symbol=symbol)
    if not orders:
        print("⚠️ No pending orders to cancel.")
        return

    for o in orders:
        if o.magic != magic:
            continue
        cancel_pending_order(o.ticket)
