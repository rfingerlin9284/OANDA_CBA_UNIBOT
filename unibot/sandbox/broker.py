from dataclasses import dataclass, field
from .instrumentation import jlog
@dataclass
class Order:
    id:int; symbol:str; side:str; size:float; entry:float; tp:float; sl:float; status:str="OPEN"
@dataclass
class Account:
    base_equity:float=10000.0; equity:float=10000.0; orders:list=field(default_factory=list)
class SandboxBroker:
    def __init__(self,symbol:str):
        self.symbol=symbol; self.acc=Account(); self._next=1
        jlog("broker.connectivity",symbol=symbol,ok=True,bypass="SIMULATED")
    def place_order(self,side,size,entry,tp,sl):
        if tp is None or sl is None:
            jlog("order.rejected",reason="TP/SL required"); return {"status":"REJECTED"}
        oid=self._next; self._next+=1
        self.acc.orders.append(Order(oid,self.symbol,side,size,entry,tp,sl))
        jlog("order.placed",id=oid,side=side,size=size,entry=entry,tp=tp,sl=sl)
        conf={"order_id":oid,"status":"FILLED","avg_fill":entry}; jlog("order.confirm",**conf); return conf
    def mark(self,price:float):
        for o in self.acc.orders:
            if o.status!="OPEN": continue
            if o.side=="LONG":
                if price>=o.tp: o.status="CLOSED_TP"
                elif price<=o.sl: o.status="CLOSED_SL"
            else:
                if price<=o.tp: o.status="CLOSED_TP"
                elif price>=o.sl: o.status="CLOSED_SL"
        unreal=0.0
        for o in self.acc.orders:
            if o.status=="OPEN":
                mult=1.0 if o.side=="LONG" else -1.0
                unreal+=(price-o.entry)*mult*o.size
        self.acc.equity=self.acc.base_equity+unreal
    def positions(self):
        net=0.0
        for o in self.acc.orders:
            if o.status=="OPEN": net+= o.size if o.side=="LONG" else -o.size
        return {"symbol":self.symbol,"net_size":net,"equity":self.acc.equity}
    def open_orders(self):
        return [o.__dict__ for o in self.acc.orders if o.status=="OPEN"]
