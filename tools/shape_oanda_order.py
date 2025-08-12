#!/usr/bin/env python3
"""
Read simple order JSON and output OANDA order payload with OCO TP/SL.
Usage: echo '{"side":"buy","instrument":"EUR_USD","entry_price":1.2754,"units":10000,"tp_pips":28,"sl_pips":15}' | tools/shape_oanda_order.py -
"""
import sys, json, uuid
from decimal import Decimal

def shape(order):
    side = order['side'].lower()
    instr = order['instrument']
    entry = Decimal(str(order['entry_price']))
    units = int(order['units'])
    tp_price = Decimal(str(order['tp_price']))
    sl_price = Decimal(str(order['sl_price']))
    payload = {
        "order": {
            "instrument": instr,
            "units": units if side == 'buy' else -units,
            "type": "MARKET",
            "timeInForce": "FOK",
            "positionFill": "DEFAULT",
            "takeProfitOnFill": {"price": f"{tp_price:.5f}"},
            "stopLossOnFill": {"price": f"{sl_price:.5f}"},
            "clientExtensions": {"id": str(uuid.uuid4())}
        }
    }
    return payload

def main():
    data = json.load(sys.stdin if sys.argv[1] == '-' else open(sys.argv[1]))
    payload = shape(data)
    print(json.dumps(payload, indent=2))

if __name__ == '__main__':
    main()
