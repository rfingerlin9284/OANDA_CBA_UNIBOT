#!/usr/bin/env bash
set -euo pipefail
source .env.live
if [ $# -eq 0 ]; then
  echo "Usage: $0 order.json" >&2; exit 1
fi
ORDER_JSON="$1"
TMP_ORDER=$(mktemp)
# Enforce OCO policy
tools/oco_guard.py "$ORDER_JSON" > "$TMP_ORDER"
# Shape into OANDA payload
PAYLOAD=$(tools/shape_oanda_order.py "$TMP_ORDER")
rm "$TMP_ORDER"
# Send to OANDA
curl -sS -X POST \
  -H "Authorization: Bearer $OANDA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "$OANDA_API_URL/v3/accounts/$OANDA_ACCOUNT_ID/orders" | jq .
