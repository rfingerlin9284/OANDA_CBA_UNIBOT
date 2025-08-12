#!/usr/bin/env bash
set -euo pipefail

# --- LIVE credentials ---
KEY="${OANDA_LIVE_API_KEY}"
ACC='001-001-13473069-001'
HOST='api-fxtrade.oanda.com'
PAIR='EUR_USD'

# --- Position details ---
UNITS='52000'       # Full size of your long
TP='1.1680'
SL='1.1643'
TAG='RBOTzilla_FORCE_OCO'

# --- Dependencies ---
command -v jq >/dev/null || { sudo apt-get update -y >/dev/null 2>&1; sudo apt-get install -y jq >/dev/null 2>&1; }

echo "✅ Using LIVE account $ACC, instrument $PAIR, units $UNITS"
echo "   TP=$TP  SL=$SL  (REDUCE_ONLY)  tag=$TAG"

# --- Place SELL LIMIT TP (reduce-only) ---
TP_PAYLOAD=$(cat <<JSON
{"order":{"type":"LIMIT","instrument":"$PAIR","units":"-$UNITS","price":"$TP","timeInForce":"GTC","positionFill":"REDUCE_ONLY","clientExtensions":{"tag":"$TAG","comment":"TP reduce-only"}}}
JSON
)
curl -sS -X POST "https://$HOST/v3/accounts/$ACC/orders" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "$TP_PAYLOAD" | jq

# --- Place SELL STOP SL (reduce-only) ---
SL_PAYLOAD=$(cat <<JSON
{"order":{"type":"STOP","instrument":"$PAIR","units":"-$UNITS","price":"$SL","timeInForce":"GTC","positionFill":"REDUCE_ONLY","clientExtensions":{"tag":"$TAG","comment":"SL reduce-only"}}}
JSON
)
curl -sS -X POST "https://$HOST/v3/accounts/$ACC/orders" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "$SL_PAYLOAD" | jq

# --- Show pending orders by tag ---
echo "→ Pending orders (tag=$TAG):"
curl -sS -H "Authorization: Bearer $KEY" "https://$HOST/v3/accounts/$ACC/pendingOrders" \
  | jq --arg tag "$TAG" '.orders // [] | map(select(.clientExtensions?.tag==$tag) | {id,type,price,units})'
