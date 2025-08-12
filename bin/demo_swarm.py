#!/usr/bin/env python3
from swarm.core.commander import SwarmCommander, SwarmConfig
from swarm.core.policy import RiskPolicy
from utils.line_renderer import render_trade_line

class PrintBroker:
    def __init__(self, px): self._px=px; self.open=[]
    def price(self, sym): return self._px
    def place_market_with_oco(self, sym, side, units, tp, sl, tags):
        t=f"D{len(self.open)+1:05d}"; self.open.append(dict(ticket=t,side=side,units=units,avg=self._px,tp=tp,sl=sl)); 
        print(render_trade_line({"status":"open","ticket":t,"symbol":sym,"side":side,"units":units,"avg":self._px,"current":self._px,"pl_pips":0.0,"oco":{"tp":tp,"sl":sl,"trailing":False,"tp_removed":False}}))
        return t
    def list_open(self, sym): return self.open
    def ensure_oco(self, ticket, tp, sl):
        for o in self.open:
            if o["ticket"]==ticket: o["tp"]=tp; o["sl"]=sl
    def trailing_sl(self, ticket, new_sl):
        for o in self.open:
            if o["ticket"]==ticket: o["sl"]=new_sl

def sample_candles():
    # (o,h,l,c) ... simple toy data to trigger an FVG
    return [
        (1.1600,1.1610,1.1595,1.1608),
        (1.1608,1.1612,1.1604,1.1610),
        (1.1609,1.16095,1.1606,1.16065),
    ]

if __name__=="__main__":
    px=1.16055
    bro=PrintBroker(px)
    cmd=SwarmCommander(bro, risk=RiskPolicy(min_sl_pips=10.0, tp_rr=1.2), cfg=SwarmConfig())
    d=cmd.evaluate_and_trade("EUR/USD","short", sample_candles(), equity_usd=1355.0, existing_adds=0)
    print("decision:", d)
