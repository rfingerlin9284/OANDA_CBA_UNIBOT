import json
import time

def check_oco_status(orders):
    alerts = []
    for o in orders:
        if not (o.get("stop_loss") and o.get("take_profit") and o.get("oco")):
            alerts.append(f"❌ OCO Missing for Order {o.get('ticket')}")
        else:
            alerts.append(f"✅ OCO Validated for Order {o.get('ticket')}")
    return alerts

if __name__ == "__main__":
    from router_live_hardcoded import fetch_open_orders
    while True:
        orders = fetch_open_orders()
        for msg in check_oco_status(orders):
            print("[OCO CHECK]", msg)
        time.sleep(60)
