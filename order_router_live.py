import requests, json, datetime

OANDA_TOKEN = "9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
OANDA_ACCOUNT = "001-001-13473069-001"
OANDA_API = "https://api-fxtrade.oanda.com/v3"

def execute_real_oanda_trade(signal):
    headers = {
        "Authorization": f"Bearer {OANDA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "order": {
            "units": str(signal["units"]),
            "instrument": signal["pair"].replace("/","_"),
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "takeProfitOnFill": {"price": str(signal["tp"])},
            "stopLossOnFill":   {"price": str(signal["sl"])}
        }
    }
    try:
        print(f"[{datetime.datetime.now()}] ➡️ [ORDER] {payload}")
        r = requests.post(f"{OANDA_API}/accounts/{OANDA_ACCOUNT}/orders", headers=headers, data=json.dumps(payload))
        if r.status_code in (200,201):
            resp = r.json()
            print(f"[{datetime.datetime.now()}] ✅ LIVE OANDA ORDER PLACED: {resp.get('orderFillTransaction', {}).get('instrument','?')} | ID: {resp.get('orderFillTransaction',{}).get('id','?')}")
            return {"success":True, "response":resp}
        else:
            print(f"[{datetime.datetime.now()}] ❌ OANDA ORDER ERROR: {r.status_code} - {r.text}")
            return {"success":False, "error":r.text}
    except Exception as e:
        print(f"[{datetime.datetime.now()}] ❌ OANDA ORDER EXCEPTION: {e}")
        return {"success":False, "error":str(e)}
