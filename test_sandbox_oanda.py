import os
from unibot.core.router import one_shot_entry

# --- config ---
symbol   = os.getenv("TEST_SYMBOL","EUR/USD")
side     = os.getenv("TEST_SIDE","buy")
units    = int(os.getenv("TEST_UNITS","100"))        # tiny
price    = float(os.getenv("TEST_PRICE","1.10000"))  # used for guard math; market ignores
pip_val  = float(os.getenv("TEST_PIP","0.0001"))

print("TRADING_MODE:", os.getenv("TRADING_MODE","(unset)"))
r = one_shot_entry(symbol, side, units, price, pip_val, open_count=0, last_fill=None)
print(r)
