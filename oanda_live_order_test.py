import oandapyV20
import oandapyV20.endpoints.orders as orders

# HARD CODE LIVE CREDS (from .env file)
OANDA_API_KEY = "bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48"
OANDA_ACCOUNT_ID = "001-001-13473069-001"
OANDA_ENV = "live"

api = oandapyV20.API(access_token=OANDA_API_KEY, environment=OANDA_ENV)

order_data = {
    "order": {
        "instrument": "EUR_USD",
        "units": "1",   # MINIMAL RISK: 1 micro lot
        "type": "MARKET",
        "positionFill": "DEFAULT"
    }
}

try:
    r = orders.OrderCreate(OANDA_ACCOUNT_ID, data=order_data)
    result = api.request(r)
    print("✅ OANDA LIVE ORDER SUCCESS:", result)
except Exception as e:
    print("❌ OANDA ORDER ERROR:", e)
