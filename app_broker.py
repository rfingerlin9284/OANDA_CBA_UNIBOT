# Minimal adapter your existing live router should satisfy.
# Replace the body to call your real OANDA/CBA functions.
from typing import List, Dict, Any
_last=1.16055

class DummyBroker:
    def price(self, symbol:str)->float:
        return _last
    def place_market_with_oco(self, symbol:str, side:str, units:int, tp:float, sl:float, tags:dict)->str:
        return "TICKET-DEMO"
    def list_open(self, symbol:str)->List[Dict[str,Any]]:
        return []
    def ensure_oco(self, ticket:str, tp:float, sl:float)->None:
        pass
    def trailing_sl(self, ticket:str, new_sl:float)->None:
        pass

broker = DummyBroker()
