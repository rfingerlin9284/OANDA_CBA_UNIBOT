#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT/.venv/bin/activate"
CFG="$ROOT/config/accelerated_replay.yaml"

# creds prompt (once) for OANDA data + practice trade
ENV_O="$ROOT/config/oanda_sandbox.env"
if [ ! -f "$ENV_O" ]; then
  read -rp "OANDA PRACTICE Account ID: " ACCT
  read -rsp "OANDA PRACTICE API Key: " KEY; echo
  cat > "$ENV_O" <<EOF
OANDA_API_BASE=https://api-fxpractice.oanda.com
OANDA_STREAM_URL=https://stream-fxpractice.oanda.com
OANDA_ACCOUNT_ID=${ACCT}
OANDA_API_KEY=${KEY}
TRADING_MODE=SANDBOX
EOF
  echo "[*] Wrote $ENV_O"
fi
set -a; source "$ENV_O"; set +a

echo "[*] Accelerated data fetch + replay (this will loop symbols; grab coffee)…"
python3 -m accelerator.engine.replay

# Real practice proof?
python3 - <<'PY'
import yaml, os, sys
cfg=yaml.safe_load(open(os.path.join(os.path.dirname(__file__),"config","accelerated_replay.yaml")))
print("practice_live_check:", cfg["global"]["practice_live_check"])
PY

if [ "$(python3 - <<'PY'
import yaml, os
cfg=yaml.safe_load(open(os.path.join(os.path.dirname(__file__),"config","accelerated_replay.yaml")))
print("1" if cfg["global"]["practice_live_check"] else "0")
PY
)" = "1" ]; then
  echo "[*] Placing ONE tiny OANDA practice order with TP/SL attached…"
  python3 -m accelerator.engine.live_practice_check
else
  echo "[*] Skipping practice wire check by config."
fi

echo
echo "=== DONE ==="
echo "Reports in: $ROOT/reports/"
echo " - ACCELERATED_BRIEF.md"
echo " - strat_metrics.json, sys_metrics.json, all_trades.csv (if any)"
