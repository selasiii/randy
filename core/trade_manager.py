# trade_manager.py

import MetaTrader5 as mt5
from datetime import datetime
from core.order_executor import place_pending_order  # ✅ correct import
from utils.pip_utils import pips_to_price            # ✅ also missing earlier


def place_zone_orders(symbol, direction, lower, upper, spacing_pips, sl_price, tp_price, lot, magic):
    """
    Place multiple stop-style pending orders inside a price zone.

    :param symbol: Trading symbol (e.g. "XAUUSD")
    :param direction: "buy" or "sell"
    :param lower: Lower bound of zone
    :param upper: Upper bound of zone
    :param spacing_pips: Distance between orders in pips
    :param sl_price: Stop loss (absolute price)
    :param tp_price: Take profit (absolute price)
    :param lot: Lot size
    :param magic: Magic number
    """
    if lower >= upper:
        print("❌ Invalid zone: lower must be < upper")
        return

    pip_step = pips_to_price(symbol, spacing_pips)

    # Generate price levels within the zone
    levels = []
    price = lower
    while price <= upper:
        levels.append(round(price, 5))  # round to avoid float drift
        price += pip_step

    # Choose order type based on direction
    if direction == "buy":
        order_type = mt5.ORDER_TYPE_BUY_LIMIT
    else:
        order_type = mt5.ORDER_TYPE_SELL_LIMIT
        levels.reverse()  # sellers stack from top → bottom

    # Dry-run preview
    print("\n📊 Zone Order Preview")
    print(f"Symbol: {symbol}")
    print(f"Direction: {direction.upper()} STOP")
    print(f"Zone: {lower} → {upper}")
    print(f"Spacing: {spacing_pips} pips")
    print(f"Orders to be placed: {len(levels)}")
    print(f"Lot size: {lot}")
    print(f"SL: {sl_price}, TP: {tp_price}")
    print(f"Magic: {magic}")
    print("Levels:", levels)

    confirm = input("\nProceed with order placement? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Zone order placement cancelled.")
        return

    # Place orders
    placed, failed = 0, 0
    for entry_price in levels:
        ticket = place_pending_order(
            symbol=symbol,
            order_type=order_type,
            lot=lot,
            entry_price=entry_price,
            sl_price=sl_price,
            tp_price=tp_price,
            magic=magic,
        )

        if ticket:
            placed += 1
            print(f"✅ Pending {direction.upper()} STOP at {entry_price} | SL={sl_price}, TP={tp_price} (ticket={ticket})")
        else:
            failed += 1
            print(f"❌ Failed to place order at {entry_price}")

    print(f"\n📊 Zone order summary for {symbol}: {placed} placed, {failed} failed "
          f"({direction.upper()} STOP, zone {lower} → {upper}, spacing={spacing_pips} pips)\n")
