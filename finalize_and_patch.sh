#!/usr/bin/env bash
set -euo pipefail
set -o errtrace
trap 'rc=$?; echo "❌ Error $rc on line $LINENO: $BASH_COMMAND" >&2' ERR

say(){ printf "\n\033[1;36m%s\033[0m\n" "$*"; }
ok(){  printf "\033[1;32m%s\033[0m\n" "$*"; }
warn(){ printf "\033[1;33m%s\033[0m\n" "$*"; }
die(){  printf "\033[1;31m✖ %s\033[0m\n" "$*"; exit 1; }

ROOT="$(pwd)"

say "0) Cleanup/dirs"
mkdir -p tools scripts config .githooks

say "1) Check secrets_replace.json"
[ -f "${ROOT}/secrets_replace.json" ] || die "Missing secrets_replace.json"
if ! command -v jq >/dev/null 2>&1; then sudo apt-get update -y && sudo apt-get install -y jq; fi
get(){ jq -r --arg k "$1" '.[$k] // empty' "${ROOT}/secrets_replace.json"; }

# OANDA
OANDA_API_TOKEN="$(get OANDA_API_TOKEN)"
OANDA_ACCOUNT_ID="$(get OANDA_ACCOUNT_ID)"
OANDA_API_URL="$(get OANDA_API_URL)"
OANDA_ENV="$(get OANDA_ENV)"; OANDA_ENV="${OANDA_ENV:-live}"
# Coinbase (HMAC key auth)
CB_API_KEY="$(get COINBASE_API_KEY)"
CB_API_SECRET="$(get COINBASE_API_SECRET)"
CB_PASSPHRASE="$(get COINBASE_PASSPHRASE)"
CB_API_URL="$(get COINBASE_API_URL)"

[[ -n "$OANDA_API_TOKEN" ]] || warn "OANDA_API_TOKEN is empty"
[[ -n "$OANDA_ACCOUNT_ID" ]] || warn "OANDA_ACCOUNT_ID is empty"
[[ -n "$CB_API_KEY"      ]] || warn "COINBASE_API_KEY is empty"
[[ -n "$CB_API_SECRET"   ]] || warn "COINBASE_API_SECRET is empty"

say "2) Write mandatory OCO policy"
cat > config/oco_policy.env <<'ENV'
# ===== Mandatory OCO policy (fail-closed) =====
OCO_MIN_SL_PIPS=6
OCO_MIN_TP_PIPS=8
OCO_MAX_SL_PIPS=300
OCO_MAX_TP_PIPS=1000
OCO_SL_ATR_MULT=1.2
OCO_TP_ATR_MULT=1.8
OCO_STRONG_TREND_TP_BONUS_PIPS=6
OCO_STAGNANT_MINUTES=25
OCO_STAGNANT_TIGHTEN_PIPS=5
OCO_GLOBAL_MAX_SL_PIPS=30
OCO_TRAIL_TRIGGER_PIPS=12
OCO_TRAIL_LOCK_PIPS=6
OCO_FAIL_CLOSED=true
ENV

say "3) Build .env.live / .env.coinbase"
cat > .env.live <<ENV
OANDA_ENV=${OANDA_ENV}
OANDA_API_URL=${OANDA_API_URL:-https://api-fxtrade.oanda.com}
OANDA_API_TOKEN=${OANDA_API_TOKEN}
OANDA_ACCOUNT_ID=${OANDA_ACCOUNT_ID}
ENV
chmod 600 .env.live

cat > .env.coinbase <<ENV
COINBASE_API_URL=${CB_API_URL:-https://api.coinbase.com}
COINBASE_API_KEY=${CB_API_KEY}
COINBASE_API_SECRET=${CB_API_SECRET}
COINBASE_PASSPHRASE=${CB_PASSPHRASE}
ENV
chmod 600 .env.coinbase

say "4) Install OCO guard (blocks orders without TP/SL)"
cat > tools/oco_guard.py <<'PY'
#!/usr/bin/env python3
import sys, json

def die(m): print(f"✖ OCO guard: {m}", file=sys.stderr); sys.exit(1)
if len(sys.argv)!=2: die("usage: tools/oco_guard.py /path/order.json")
try: order=json.load(open(sys.argv[1]))
except Exception as e: die(f"cannot read order json: {e}")

def load_env(path):
    d={}
    try:
        with open(path) as f:
            for ln in f:
                ln=ln.strip()
                if not ln or ln.startswith("#"): continue
                if "=" in ln:
                    k,v=ln.split("=",1); d[k.strip()]=v.strip()
    except FileNotFoundError: pass
    return d
cfg = {}
for p in ("config/oco_policy.env",".env.live"): cfg.update(load_env(p))

def geti(k, d): 
    try: return int(float(cfg.get(k,d)))
    except: return int(d)
def getf(k, d):
    try: return float(cfg.get(k,d))
    except: return float(d)

FAIL = str(cfg.get("OCO_FAIL_CLOSED","true")).lower()=="true"
MIN_SL,MIN_TP = geti("OCO_MIN_SL_PIPS",6),  geti("OCO_MIN_TP_PIPS",8)
MAX_SL,MAX_TP = geti("OCO_MAX_SL_PIPS",300), geti("OCO_MAX_TP_PIPS",1000)
SL_M,TP_M     = getf("OCO_SL_ATR_MULT",1.2), getf("OCO_TP_ATR_MULT",1.8)
TP_BON        = geti("OCO_STRONG_TREND_TP_BONUS_PIPS",6)
GLOBAL_MAX_SL = geti("OCO_GLOBAL_MAX_SL_PIPS",30)

atr   = float(order.get("atr") or 0.0)
trend = int(order.get("trend_strength") or 0)
tp,sl = order.get("tp_pips"), order.get("sl_pips")

if sl in (None,""): sl = max(MIN_SL, round(SL_M*atr)) if atr>0 else MIN_SL
if tp in (None,""):
    base = max(MIN_TP, round(TP_M*atr)) if atr>0 else MIN_TP
    if trend>=2: base += TP_BON
    tp = base

sl = min(max(int(sl),MIN_SL),MAX_SL)
tp = min(max(int(tp),MIN_TP),MAX_TP)
sl = min(sl, GLOBAL_MAX_SL)

if FAIL and (not sl or not tp): die("blocked: missing TP/SL")
order["sl_pips"]=float(sl); order["tp_pips"]=float(tp)
print(json.dumps(order, separators=(',',':')))
PY
chmod +x tools/oco_guard.py

say "5) Optional JWT helper (HS256)"
cat > tools/jwt_hs256.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
# usage: ./tools/jwt_hs256.sh <secret> <claims-json>
b64url(){ openssl base64 -A | tr '+/' '-_' | tr -d '='; }
s="$1"; claims="$2"
hdr='{"alg":"HS256","typ":"JWT"}'
h="$(printf '%s' "$hdr"   | b64url)"
p="$(printf '%s' "$claims"| b64url)"
sig="$(printf '%s' "$h.$p" | openssl dgst -sha256 -hmac "$s" -binary | b64url)"
printf '%s.%s.%s\n' "$h" "$p" "$sig"
SH
chmod +x tools/jwt_hs256.sh

say "6) API smoke checks"
cat > scripts/verify_apis.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
source .env.live
source .env.coinbase
echo "== OANDA account summary =="
curl -sS -H "Authorization: Bearer ${OANDA_API_TOKEN}" \
     -H "Content-Type: application/json" \
     "${OANDA_API_URL}/v3/accounts/${OANDA_ACCOUNT_ID}/summary" | head -n 80
echo
echo "== Coinbase time ping =="
curl -sS -H "CB-ACCESS-KEY: ${COINBASE_API_KEY}" \
     "${COINBASE_API_URL}/v2/time" | head -n 40
SH
chmod +x scripts/verify_apis.sh

say "7) Pre-commit guard"
cat > .githooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail
# block PEM/JWT
if git diff --cached -U0 | grep -E 'BEGIN [^-]*PRIVATE KEY|[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+' >/dev/null; then
  echo "✖ Abort: key or JWT-like token detected in commit."; exit 1; fi
# block .env / secrets_*
if git diff --cached --name-only | grep -E '(^|/)(\.env(\.|$)|secrets_.*\.json)$' >/dev/null; then
  echo "✖ Abort: .env / secrets_* must not be committed."; exit 1; fi
HOOK
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks

say "✔ Done"
ok  "-> .env.live / .env.coinbase"
ok  "-> config/oco_policy.env"
ok  "-> tools/oco_guard.py"
ok  "-> tools/jwt_hs256.sh"
ok  "-> scripts/verify_apis.sh"
ok  "-> pre-commit guard"
printf "\nTry:\n"
printf "  source .env.live\n"
printf "  cat > /tmp/order.json <<'JSON'\n"
printf "  {\"side\":\"buy\",\"entry_price\":1.27540,\"atr\":12.3,\"trend_strength\":2}\n"
printf "  JSON\n"
printf "  tools/oco_guard.py /tmp/order.json\n\n"
printf "  ./scripts/verify_apis.sh\n"
