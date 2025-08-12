#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
RUN_ID="${RUN_ID:-$(date +%Y%m%d_%H%M%S)}"
LOG_DIR="$ROOT/logs/sandbox/$RUN_ID"
mkdir -p "$LOG_DIR"
while IFS= read -r line; do
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  export "$line"
done < "$ROOT/envs/.env.sandbox"
export MODE="${MODE:-SANDBOX}"
export SYMBOL="${SYMBOL:-EUR_USD}"
export LOG_FILE="${LOG_FILE:-$LOG_DIR/flow.jsonl}"
python3 -m unibot.sandbox.runner ${1:+--csv "$1"} 2>&1 | tee "$LOG_DIR/stdout.log"
echo ">> DONE. Run label: $RUN_ID"
echo "Tail logs: tail -f \"$LOG_DIR/flow.jsonl\""
