import time, json, requests, base64
from nacl import signing

CB_API_KEY    = "bbd70034-6acb-4c1c-8d7a-4358a434ed4b"
CB_API_SECRET = "yN8Q2bgm7bCGlLptrbixoGO+SIUu1cfyVyh/uTzk4BGXGzz1IrbEBBFJa+6dw4O3Ar4pkbWKW1SOeUB/r8n1kg=="
CB_API_URL    = "https://api.coinbase.com/api/v3/brokerage/orders"

def ed25519_sign(msg, secret):
    key = signing.SigningKey(base64.b64decode(secret))
    return base64.b64encode(key.sign(msg.encode("utf-8")).signature).decode("utf-8")

def place_coinbase_order(pair, side, size, price=None):
    ts = str(int(time.time()))
    order = {
        "client_order_id": f"rbot-{int(time.time()*1000)}",
        "product_id": pair,
        "side": side.lower(),
        "order_configuration": {
            "market_market_ioc": {
                "base_size": str(size)
            }
        }
    }
    payload = json.dumps(order)
    msg = ts + "POST" + "/api/v3/brokerage/orders" + payload
    sig = ed25519_sign(msg, CB_API_SECRET)
    headers = {
        "Content-Type": "application/json",
        "CB-ACCESS-KEY": CB_API_KEY,
        "CB-ACCESS-SIGN": sig,
        "CB-ACCESS-TIMESTAMP": ts
    }
    try:
        print(f"[{ts}] ➡️ [COINBASE ORDER] {order}")
        r = requests.post(CB_API_URL, headers=headers, data=payload)
        if r.status_code in (200,201):
            print(f"[{ts}] ✅ LIVE COINBASE ORDER PLACED: {pair} | {side.upper()} | {r.json()}")
            return {"success":True, "response":r.json()}
        else:
            print(f"[{ts}] ❌ COINBASE ORDER ERROR: {r.status_code} - {r.text}")
            return {"success":False, "error":r.text}
    except Exception as e:
        print(f"[{ts}] ❌ COINBASE ORDER EXCEPTION: {e}")
        return {"success":False, "error":str(e)}
