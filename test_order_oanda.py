import requests, json

ACCOUNT_ID = "001-001-13473069-001"
TOKEN = "9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
OANDA_URL = f"https://api-fxtrade.oanda.com/v3/accounts/{ACCOUNT_ID}/orders"

instrument = "EUR_USD"
units = "2000"
tp = "1.2000"
sl = "1.1000"

order_data = {
    "order": {
        "type": "MARKET",
        "instrument": instrument,
        "units": units,
        "positionFill": "DEFAULT",
        "timeInForce": "FOK",
        "takeProfitOnFill": {
            "price": tp,
            "timeInForce": "GTC"
        },
        "stopLossOnFill": {
            "price": sl,
            "timeInForce": "GTC"
        }
    }
}
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("\n=== OANDA ORDER PAYLOAD ===")
print(json.dumps(order_data, indent=2))
r = requests.post(OANDA_URL, headers=headers, json=order_data)
print("\n=== OANDA RESPONSE ===")
print(r.status_code, r.text)
with open("logs/oanda_test_order_response.log", "a") as f:
    f.write(f"{r.status_code} | {r.text}\n")
