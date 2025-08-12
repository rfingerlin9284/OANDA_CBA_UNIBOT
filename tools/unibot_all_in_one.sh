#!/usr/bin/env bash
# To run this script:
#   ./unibot_all_in_one.sh               # synthetic feed
#   ./unibot_all_in_one.sh data/eurusd_5m.csv   # with CSV (columns: ts,open,high,low,close)
set -euo pipefail

# ------------- SETTINGS -------------
PROJECT_NAME="OANDA_CBA_UNIBOT"
ROOT="$(pwd)"
RUN_ID="${RUN_ID:-$(date +%Y%m%d_%H%M%S)}"
LOG_DIR="$ROOT/logs/sandbox/$RUN_ID"
TOOLS_DIR="$ROOT/tools"
ENV_DIR="$ROOT/envs"
DATA_DIR="$ROOT/data"
RELEASE_DIR="$ROOT/releases/sandbox/$RUN_ID"
LIVE_PARENT="$(dirname "$ROOT")"
LIVE_CLONE="$LIVE_PARENT/${PROJECT_NAME}_LIVE_${RUN_ID}"

CSV_PATH="${1:-}"   # optional CSV path

# ------------- PREP FOLDERS -------------
mkdir -p "$ROOT/unibot/sandbox" "$ROOT/unibot" "$ENV_DIR" "$DATA_DIR" "$LOG_DIR" "$TOOLS_DIR" "$RELEASE_DIR" "$ROOT/releases"

# ------------- WRITE SANDBOX PACKAGE (NO TA-LIB) -------------
cat > "$ROOT/unibot/__init__.py" << "PY"
# UNIBOT package marker
PY

cat > "$ROOT/unibot/sandbox/__init__.py" << "PY"
"""
UNIBOT Sandbox: headless pretend-live mode (no external API calls).
"""
PY

cat > "$ROOT/unibot/sandbox/instrumentation.py" << "PY"
import json, os, time, threading, pathlib
_lock = threading.Lock()
def jlog(event, **ctx):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
           "event": event, "mode": os.getenv("MODE","SANDBOX"), **ctx}
    line = json.dumps(rec, separators=(",",":"))
    print(line, flush=True)
    log_file = os.getenv("LOG_FILE")
    if log_file:
        pathlib.Path(os.path.dirname(log_file)).mkdir(parents=True, exist_ok=True)
        with _lock, open(log_file, "a", encoding="utf-8") as f: f.write(line+"\n")
PY

cat > "$ROOT/unibot/sandbox/feed.py" << "PY"
import csv, random
def load_csv(path):
    with open(path,"r",newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            yield {"ts":row.get("ts"),
                   "o":float(row["open"]),"h":float(row["high"]),
                   "l":float(row["low"]),"c":float(row["close"])}
def synthetic(n=2000,start=1.10000,vol=0.0005):
    price=start
    for i in range(n):
        ret=random.gauss(0.0,vol)
        o=price; c=o*(1.0+ret)
        hi=max(o,c)*(1.0+abs(random.gauss(0,vol/2)))
        lo=min(o,c)*(1.0-abs(random.gauss(0,vol/2)))
        price=c
        yield {"ts":str(i),"o":o,"h":hi,"l":lo,"c":c}
PY

cat > "$ROOT/unibot/sandbox/mathlib.py" << "PY"
import math
def sma(v,p):
    if p<=0 or len(v)<p: return float("nan")
    return sum(v[-p:])/float(p)
def zscore(v,p):
    if p<=1 or len(v)<p: return 0.0
    w=v[-p:]; mu=sum(w)/p
    var=sum((x-mu)**2 for x in w)/(p-1)
    sd=math.sqrt(max(var,1e-12))
    return (v[-1]-mu)/sd
def true_range(o,h,l,pc): return max(h-l, abs(h-pc), abs(l-pc))
def atr(ohlc,p):
    if len(ohlc)<p+1: return 0.0
    trs=[]
    for i in range(1,len(ohlc)):
        o,h,l,c=ohlc[i]; _,_,_,pc=ohlc[i-1]
        trs.append(true_range(o,h,l,pc))
    if len(trs)<p: return 0.0
    return sum(trs[-p:])/p
PY

cat > "$ROOT/unibot/sandbox/signals.py" << "PY"
from .mathlib import sma, zscore
def detect_fvg(ohlc, lookback=50):
    n=len(ohlc); bull=bear=0.0; gap=0.0
    if n<3: return {"bull":0.0,"bear":0.0,"gap":0.0}
    start=max(2,n-lookback)
    for i in range(start,n):
        if i<2: continue
        _,hi2,lo2,_=ohlc[i-2]; o,h,l,c=ohlc[i]
        if l>hi2: bull=1.0; gap=max(gap,l-hi2)
        if h<lo2: bear=1.0; gap=max(gap,lo2-h)
    return {"bull":bull,"bear":bear,"gap":gap}
def momentum_weight(closes,fast,slow):
    sf=sma(closes,fast); ss=sma(closes,slow)
    if sf!=sf or ss!=ss: return 0.0
    base=0.0 if ss==0 else (sf-ss)/abs(ss)
    base=max(-0.02,min(0.02,base))
    return (base+0.02)/0.04
def meanrev_weight(closes,p):
    z=zscore(closes,p); z=max(-3.0,min(3.0,z))
    return min(1.0,abs(z)/3.0)
def aggregate_signal(ohlc,w_fvg,w_mom,w_mr,fvg_lb,fast,slow,mr_p):
    closes=[c for _,_,_,c in ohlc]
    fvgr=detect_fvg(ohlc,fvg_lb)
    mom=momentum_weight(closes,fast,slow)
    mr=meanrev_weight(closes,mr_p)
    mom_dir=1.0 if (sma(closes,fast)>sma(closes,slow)) else -1.0
    dir_score=(fvgr["bull"]-fvgr["bear"])+0.5*mom_dir
    side="LONG" if dir_score>=0 else "SHORT"
    conf=max(0.0,min(1.0, w_fvg*(fvgr["bull"] or fvgr["bear"])+w_mom*mom+w_mr*mr))
    return {"side":side,"confidence":conf,"fvg_gap":fvgr["gap"]}
PY

cat > "$ROOT/unibot/sandbox/risk.py" << "PY"
from .mathlib import atr
FIB=[0.0,0.236,0.382,0.5,0.618,0.786,1.0]
def fib_leverage(base,maxlev,conf):
    i=int(round(conf*(len(FIB)-1))); i=max(0,min(len(FIB)-1,i))
    return max(1.0, min(maxlev, base*(1.0+FIB[i]*(maxlev-1.0))))
def tp_sl_from_atr(ohlc,atr_p,tp_m,sl_m,side):
    a=atr(ohlc,atr_p); last=ohlc[-1][3]
    if side=="LONG":  return last+a*tp_m, last-a*sl_m
    else:             return last-a*tp_m, last+a*sl_m
PY

cat > "$ROOT/unibot/sandbox/broker.py" << "PY"
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
PY

cat > "$ROOT/unibot/sandbox/runner.py" << "PY"
import os, argparse
from .instrumentation import jlog
from .feed import load_csv, synthetic
from .signals import aggregate_signal
from .risk import fib_leverage, tp_sl_from_atr
from .mathlib import atr
from .broker import SandboxBroker
def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--symbol",default=os.getenv("SYMBOL","EUR_USD"))
    p.add_argument("--csv",help="CSV with ts,open,high,low,close")
    p.add_argument("--steps",type=int,default=1200)
    return p.parse_args()
def main():
    a=parse_args(); env=os.environ
    jlog("sandbox.start",symbol=a.symbol,run=os.getenv("RUN_ID"))
    stream = load_csv(a.csv) if a.csv else synthetic(a.steps)
    base=float(env.get("BASE_LEVERAGE","1")); maxlev=float(env.get("MAX_LEVERAGE","5"))
    w_fvg=float(env.get("W_FVG","0.60")); w_mom=float(env.get("W_MOMENTUM","0.25")); w_mr=float(env.get("W_MEANREV","0.15"))
    fvg_lb=int(env.get("FVG_LOOKBACK","50")); fast=int(env.get("SMA_FAST","10")); slow=int(env.get("SMA_SLOW","30"))
    mr_p=int(env.get("MR_PERIOD","50")); atr_p=int(env.get("ATR_PERIOD","14"))
    tp_m=float(env.get("TP_ATR","2.0")); sl_m=float(env.get("SL_ATR","1.2"))
    risk=float(env.get("RISK_PER_TRADE","0.01"))
    broker=SandboxBroker(a.symbol); ohlc=[]
    for i,bar in enumerate(stream):
        o,h,l,c=bar["o"],bar["h"],bar["l"],bar["c"]; ohlc.append((o,h,l,c)); broker.mark(c)
        if len(ohlc)<max(slow,mr_p,fvg_lb,atr_p)+3: continue
        sig=aggregate_signal(ohlc,w_fvg,w_mom,w_mr,fvg_lb,fast,slow,mr_p)
        aatr=atr(ohlc,atr_p); tp,sl=tp_sl_from_atr(ohlc,atr_p,tp_m,sl_m,sig["side"])
        equity=broker.positions()["equity"]; dist=abs(tp-sl); size=0.0
        if dist>0: size=(equity*risk/dist)*fib_leverage(base,maxlev,sig["confidence"])
        jlog("signal.evaluated",side=sig["side"],confidence=round(sig["confidence"],4),
             atr=aatr,tp=tp,sl=sl,size=round(size,4))
        if sig["confidence"]>=0.60 and size>0: broker.place_order(sig["side"],size,c,tp,sl)
        if (i%50)==0: jlog("account.snapshot",**broker.positions(),open_orders=len(broker.open_orders()))
    jlog("sandbox.done",**broker.positions())
if __name__=="__main__": main()
PY

# ------------- ENV (SANDBOX DEFAULTS) -------------
cat > "$ENV_DIR/.env.sandbox" << "ENV"
MODE=SANDBOX
SYMBOL=EUR_USD
BASE_LEVERAGE=1.0
MAX_LEVERAGE=5
RISK_PER_TRADE=0.01
W_FVG=0.60
W_MOMENTUM=0.25
W_MEANREV=0.15
FVG_LOOKBACK=50
ATR_PERIOD=14
SMA_FAST=10
SMA_SLOW=30
MR_PERIOD=50
TP_ATR=2.0
SL_ATR=1.2
ENV

# ------------- RUN SANDBOX ONCE (synthetic or CSV) -------------
export RUN_ID="$RUN_ID"
export MODE="SANDBOX"
export LOG_FILE="$LOG_DIR/flow.jsonl"

# Load env
while IFS= read -r line; do
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  export "$line"
done < "$ENV_DIR/.env.sandbox"

echo ">> Running sandbox... RUN_ID=$RUN_ID"
python3 -m unibot.sandbox.runner ${CSV_PATH:+--csv "$CSV_PATH"} 2>&1 | tee "$LOG_DIR/stdout.log"
echo ">> Sandbox complete."

# ------------- PACKAGE ARTIFACTS -------------
echo ">> Packaging artifacts..."
COMMIT="unknown"
if command -v git >/dev/null 2>&1; then
  COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
fi
echo "$COMMIT" > "$RELEASE_DIR/COMMIT.txt"
cp "$ENV_DIR/.env.sandbox" "$RELEASE_DIR/.env.sandbox"
cp "$LOG_DIR/flow.jsonl" "$RELEASE_DIR/flow.jsonl"
cp "$LOG_DIR/stdout.log" "$RELEASE_DIR/stdout.log"
BUNDLE="$ROOT/sandbox_artifacts_${RUN_ID}.tar.gz"
tar -czf "$BUNDLE" -C "$RELEASE_DIR" .
echo ">> Created bundle: $BUNDLE"

# ------------- PROMOTE: LIVE CLONE WITH GUARDS -------------
echo ">> Preparing LIVE clone at: $LIVE_CLONE"
rsync -a --exclude ".git" --exclude "logs" --exclude "__pycache__" "$ROOT/" "$LIVE_CLONE/"
mkdir -p "$LIVE_CLONE/envs" "$LIVE_CLONE/logs/live"

cat > "$LIVE_CLONE/envs/.env.live" << "ENV"
MODE=LIVE
LIVE_REAL_MONEY=true
SANDBOX=false
DEMO=false
PAPER=false
SIMULATION=false

# LIVE endpoints (hard-coded)
OANDA_ENV=live
OANDA_REST_BASE=https://api-fxtrade.oanda.com
OANDA_STREAM_BASE=https://stream-fxtrade.oanda.com

# REQUIRED (placeholders — set securely in shell/secrets; do NOT commit secrets)
OANDA_ACCOUNT_ID=__REPLACE_ME__
# export OANDA_API_KEY=your_key_here (in your shell, not this file)

SYMBOL=EUR_USD
BASE_LEVERAGE=1.0
MAX_LEVERAGE=5
RISK_PER_TRADE=0.005
W_FVG=0.60
W_MOMENTUM=0.25
W_MEANREV=0.15
FVG_LOOKBACK=50
ATR_PERIOD=14
SMA_FAST=10
SMA_SLOW=30
MR_PERIOD=50
TP_ATR=2.0
SL_ATR=1.2
LOG_FILE=logs/live/flow.jsonl
ENV

cat > "$LIVE_CLONE/run_live.sh" << "BASH2"
#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" != "--confirm" || "${2:-}" != "LIVE" ]]; then
  echo "Refusing to run. Usage: ./run_live.sh --confirm LIVE [--dry-run]"
  exit 1
fi
DRY="${3:-}"

# Load env
while IFS= read -r line; do
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  export "$line"
done < envs/.env.live

mkdir -p "$(dirname "$LOG_FILE")"

if [[ "$DRY" == "--dry-run" ]]; then
  python3 - <<PY
import os, json
print(json.dumps({
  "event":"live.connectivity.check",
  "rest_base":os.getenv("OANDA_REST_BASE"),
  "account_id_set": bool(os.getenv("OANDA_ACCOUNT_ID")),
  "api_key_set": bool(os.getenv("OANDA_API_KEY"))
}))
PY
  exit 0
fi

# >>> Replace the following line with your actual live entrypoint when ready:
echo "LIVE mode launcher stub: replace with real live adapter/runner call."
# Example:
# python3 -m unibot.core.router --mode LIVE
BASH2
chmod +x "$LIVE_CLONE/run_live.sh"

# ------------- SAVE A COPY OF THIS SCRIPT (EXECUTABLE) -------------
cp "$ROOT/$(basename "$0")" "$TOOLS_DIR/$(basename "$0")"
chmod +x "$TOOLS_DIR/$(basename "$0")"

# ------------- GIT COMMIT & PUSH -------------
if command -v git >/dev/null 2>&1; then
  echo ">> Git committing and pushing changes..."
  git add -A || true
  git commit -m "sandbox run $RUN_ID: add sandbox code, artifacts, and LIVE clone scaffold" || true
  if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    git push
  else
    echo "!! No upstream set for current branch; skipped push."
    echo "   To set upstream: git push -u origin \$(git branch --show-current)"
  fi
else
  echo "!! git not found; skipped commit/push."
fi

echo "------------------------------------------------------------"
echo "RUN_ID:        $RUN_ID"
echo "Sandbox logs:  $LOG_DIR/flow.jsonl"
echo "Console log:   $LOG_DIR/stdout.log"
echo "Bundle:        $BUNDLE"
echo "LIVE clone:    $LIVE_CLONE"
echo "Re-run later:  $TOOLS_DIR/$(basename "$0")"
echo "------------------------------------------------------------"
