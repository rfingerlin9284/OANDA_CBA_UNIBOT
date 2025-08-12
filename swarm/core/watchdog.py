import time
from typing import Dict, Any, Optional, List

class OcoWatchdog:
    def __init__(self, broker, check_secs:int=2, allow_tp_remove:bool=True, sl_immutable:bool=True, narrator=None):
        self.broker=broker; self.dt=check_secs; self.allow_tp_remove=allow_tp_remove; self.sl_immutable=sl_immutable; self.say=narrator or (lambda msg: print(msg))

    def loop(self, symbol:str):
        while True:
            try:
                for t in self.broker.list_open(symbol):
                    tp=t.get("tp"); sl=t.get("sl"); ticket=t["ticket"]; side=t["side"]
                    price=self.broker.price(symbol)
                    # SL must exist
                    if not sl and self.sl_immutable:
                        # restore SL at a defensive spot
                        restore = price - 0.0010 if side=="long" else price + 0.0010
                        self.broker.ensure_oco(ticket, tp if self.allow_tp_remove else (tp or (price+0.0010 if side=="long" else price-0.0010)), restore)
                        self.say(f"[OCO-ENFORCER] Restored SL on {ticket}")
                    # TP may be removed by strategy
                    if not tp and not self.allow_tp_remove:
                        # if not allowed, put a conservative TP
                        fallback = price + 0.0012 if side=="long" else price - 0.0012
                        self.broker.ensure_oco(ticket, fallback, sl or (price - 0.0010 if side=='long' else price + 0.0010))
                        self.say(f"[OCO-ENFORCER] Reinstated TP on {ticket}")
            except Exception as e:
                self.say(f"[OCO-ENFORCER] error: {e}")
            time.sleep(self.dt)
