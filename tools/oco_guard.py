#!/usr/bin/env python3
"""
Validate and shape incoming orders into OCO children according to policy.
Usage: tools/oco_guard.py /path/to/order.json
If FAIL_CLOSED=1 in environment, exits non‑zero on any missing TP/SL.
"""
import os, sys, json, decimal
from decimal import Decimal
from dotenv import load_dotenv
load_dotenv('.env.live')
load_dotenv('config/oco_policy.env')

def clamp(value, low, high):
    return max(low, min(high, value))

def main():
    if len(sys.argv) != 2:
        print("Usage: oco_guard.py order.json", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1],'r') as f:
        order = json.load(f)
    side  = order.get('side','').lower()
    price = Decimal(str(order.get('entry_price')))
    tp_pips = Decimal(str(order.get('tp_pips', 0)))
    sl_pips = Decimal(str(order.get('sl_pips', 0)))

    min_tp = Decimal(os.getenv('TP_PIPS_MIN','10'))
    max_tp = Decimal(os.getenv('TP_PIPS_MAX','60'))
    min_sl = Decimal(os.getenv('SL_PIPS_MIN','15'))
    max_sl = Decimal(os.getenv('SL_PIPS_MAX','40'))
    risk_fraction = Decimal(os.getenv('RISK_FRACTION','0.01'))
    fail_closed = int(os.getenv('FAIL_CLOSED','0'))

    if not tp_pips or not sl_pips:
        if fail_closed:
            print("✖ OCO guard: TP/SL missing and FAIL_CLOSED=1", file=sys.stderr)
            sys.exit(2)
        else:
            tp_pips = min_tp
            sl_pips = min_sl

    tp_pips = clamp(tp_pips, min_tp, max_tp)
    sl_pips = clamp(sl_pips, min_sl, max_sl)

    if side == 'buy':
        tp_price = price + tp_pips * Decimal('0.0001')
        sl_price = price - sl_pips * Decimal('0.0001')
    elif side == 'sell':
        tp_price = price - tp_pips * Decimal('0.0001')
        sl_price = price + sl_pips * Decimal('0.0001')
    else:
        print("✖ Invalid side. Must be 'buy' or 'sell'", file=sys.stderr)
        sys.exit(1)

    order['tp_price'] = float(tp_price)
    order['sl_price'] = float(sl_price)
    print(json.dumps(order, indent=2))

if __name__ == '__main__':
    decimal.getcontext().prec = 10
    main()
