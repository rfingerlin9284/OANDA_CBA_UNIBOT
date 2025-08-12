#!/usr/bin/env bash
set -euo pipefail
source .env.live
if [ $# -eq 0 ]; then
  echo "Usage: $0 order.json" >&2; exit 1
fi
ORDER_JSON="$1"
# shape into coinbase payloads
PAYLOADS=$(tools/shape_coinbase_order.py "$ORDER_JSON")
main=$(echo "$PAYLOADS" | jq -c '.main')
tp=$(echo "$PAYLOADS"   | jq -c '.tp')
sl=$(echo "$PAYLOADS"   | jq -c '.sl')
# function to sign and send
call() {
  local body="$1"
  local endpoint="/api/v3/brokerage/orders"
  local timestamp=$(date +%s)
  local method="POST"
  local message="$timestamp$method$endpoint$body"
  local secret=$(python3 -c "import os,base64;print(base64.b64decode(os.environ['CB_API_SECRET']))")
  local sig=$(echo -n "$message" | openssl dgst -sha256 -binary -mac HMAC -macopt "key:$secret" | base64)
  curl -sS -X POST "$CB_API_URL$endpoint" \
    -H "CB-ACCESS-KEY:$CB_API_KEY" \
    -H "CB-ACCESS-SIGN:$sig" \
    -H "CB-ACCESS-TIMESTAMP:$timestamp" \
    -H "CB-ACCESS-PASSPHRASE:$CB_PASSPHRASE" \
    -H "Content-Type: application/json" \
    -d "$body" | jq .
}
call "$main"
call "$tp"
call "$sl"
