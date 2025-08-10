import requests, time, hmac, hashlib, base64, json, os

# --- Replace with YOUR Coinbase API keys and passphrase ---
API_KEY = "YOUR_COINBASE_API_KEY"
API_SECRET = "YOUR_COINBASE_API_SECRET"
PASSPHRASE = "YOUR_COINBASE_PASSPHRASE"
BASE_URL = "https://api.coinbase.com"

def get_headers(method, request_path, body=""):
    timestamp = str(int(time.time()))
    message = timestamp + method + request_path + body
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode()
    return {
        'CB-ACCESS-KEY': API_KEY,
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-PASSPHRASE': PASSPHRASE,
        'Content-Type': 'application/json'
    }

# Example: Market BUY 0.001 BTC/USD
body = json.dumps({
    "size": "0.001",
    "side": "buy",
    "product_id": "BTC-USD",
    "type": "market"
})
headers = get_headers("POST", "/api/v3/brokerage/orders", body)
url = BASE_URL + "/api/v3/brokerage/orders"
print("\n=== COINBASE ORDER PAYLOAD ===")
print(body)
r = requests.post(url, headers=headers, data=body)
print("\n=== COINBASE RESPONSE ===")
print(r.status_code, r.text)
with open("logs/coinbase_test_order_response.log", "a") as f:
    f.write(f"{r.status_code} | {r.text}\n")
