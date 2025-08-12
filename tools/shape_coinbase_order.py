#!/usr/bin/env python3
"""
Convert simple order JSON into Coinbase Advanced order payload.
Usage: echo '{"side":"buy","product_id":"BTC-USD","entry_price":42000,"size":0.001,"tp_delta":500,"sl_delta":300}' | shape_coinbase_order.py -
Produces 3 orders (main, TP, SL) grouped by client_order_id.
"""
import sys, json, uuid, time
from decimal import Decimal

def shape(order):
    side = order['side'].lower()
    prod = order['product_id']
    size = Decimal(str(order['size']))
    entry = Decimal(str(order['entry_price']))
    tp_delta = Decimal(str(order['tp_delta']))
    sl_delta = Decimal(str(order['sl_delta']))
    gid = str(uuid.uuid4())
    opp = 'sell' if side == 'buy' else 'buy'
    tp_price = (entry + tp_delta) if side=='buy' else (entry - tp_delta)
    sl_price = (entry - sl_delta) if side=='buy' else (entry + sl_delta)
    main = {
        "side": side.upper(),
        "product_id": prod,
        "client_order_id": f"grp-{gid}-main",
        "order_configuration":{
          "limit_limit_gtc": {
            "base_size": str(size),
            "limit_price": str(entry),
            "post_only": False
          }
        }
    }
    tp  = {
        "side": opp.upper(),
        "product_id": prod,
        "client_order_id": f"grp-{gid}-tp",
        "order_configuration":{
          "limit_limit_gtc": {
            "base_size": str(size),
            "limit_price": str(tp_price),
            "post_only": False
          }
        }
    }
    sl  = {
        "side": opp.upper(),
        "product_id": prod,
        "client_order_id": f"grp-{gid}-sl",
        "order_configuration":{
          "limit_limit_gtc": {
            "base_size": str(size),
            "limit_price": str(sl_price),
            "post_only": False
          }
        }
    }
    return {"main":main,"tp":tp,"sl":sl}

def main():
    data = json.load(sys.stdin if sys.argv[1]=='-' else open(sys.argv[1]))
    print(json.dumps(shape(data), indent=2))

if __name__ == '__main__':
    main()
