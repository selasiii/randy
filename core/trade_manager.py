# core/trade_manager.py

import MetaTrader5 as mt5
from core.order_executor import place_pending_order
from utils.pip_utils import pips_to_price
from utils.mt5_utils import get_current_tick


def place_zone_orders(
    symbol,
    direction,
    lower_price,
    upper_price,
    spacing_pips,
    sl_price,
    tp_price,
    base_lot,
    antimartingale_enabled,
    antimartingale_mode,
    increment_step,
    exponential_factor,
    magic,
):
    if lower_price >= upper_price:
        print("❌ Invalid zone: lower must be < upper")
        return []

    pip_step = pips_to_price(symbol, spacing_pips)

    # generate levels
    levels = []
    price = lower_price
    while price <= upper_price:
        levels.append(round(price, 5))
        price += pip_step

    # decide order type depending on direction and current price
    tick = get_current_tick(symbol)
    if not tick:
        print("❌ No tick data for symbol.")
        return []

    current_price = tick.ask if direction == "buy" else tick.bid

    def resolve_order_type(entry_price):
        if direction == "buy":
            return mt5.ORDER_TYPE_BUY_LIMIT if entry_price < current_price else mt5.ORDER_TYPE_BUY_STOP
        else:
            return mt5.ORDER_TYPE_SELL_LIMIT if entry_price > current_price else mt5.ORDER_TYPE_SELL_STOP

    # preview
    print("\n📊 Zone Order Preview")
    print(f"Symbol: {symbol}, Direction: {direction.upper()}")
    print(f"Zone: {lower_price} → {upper_price}, Spacing: {spacing_pips} pips")
    print(f"Levels: {levels}")
    print(f"Anti-Martingale: {antimartingale_enabled} ({antimartingale_mode})")
    confirm = input("\nProceed with placement? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Cancelled by user.")
        return []

    # lot sizing logic
    placed_tickets = []
    for i, entry_price in enumerate(levels, start=1):
        lot = base_lot
        if antimartingale_enabled:
            if antimartingale_mode == "incremental":
                lot = base_lot + increment_step * (i - 1)
            elif antimartingale_mode == "exponential":
                lot = base_lot * (exponential_factor ** (i - 1))

        order_type = resolve_order_type(entry_price)
        ticket = place_pending_order(
            symbol=symbol,
            order_type=order_type,
            lot=lot,
            entry_price=entry_price,
            sl_price=sl_price,
            tp_price=tp_price,
            magic=magic,   # ✅ FIXED
        )
        if ticket:
            placed_tickets.append(ticket)
            print(f"✅ Placed order {ticket}: {direction.upper()} {lot} lots @ {entry_price}")
        else:
            print(f"❌ Failed at {entry_price}")

    return placed_tickets
