#!/usr/bin/env bash
set -euo pipefail

# === LIVE Credentials (hard-coded) ===
OANDA_API_KEY='9563fc3b9a1a5544ed4107a77f0c20d-47a290887d211225a30b14a9e9e58d588'
ACCOUNT_ID='001-001-13473069-001'
HOST='api-fxtrade.oanda.com'
PAIR='EUR_USD'

# === TP/SL + trailing settings ===
TP=1.1680
SL=1.1643
BUFFER=0.0004    # SL stays ~4 pips behind bid
STEP=0.0005      # trail every 5 pips
LOG_FILE="runner_mode.log"

log_event(){ echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"; }

# 1) Attach TP/SL to all open EUR_USD trades
TRADE_IDS=$(curl -sS -H "Authorization: Bearer $OANDA_API_KEY" \
  "https://$HOST/v3/accounts/$ACCOUNT_ID/openTrades" \
  | jq -r --arg sym "$PAIR" '.trades // [] | map(select(.instrument==$sym) | .id) | .[]')

if [ -z "$TRADE_IDS" ]; then
  log_event "No open $PAIR trades found. Exiting."
  exit 0
fi

for T in $TRADE_IDS; do
  curl -sS -X PUT "https://$HOST/v3/accounts/$ACCOUNT_ID/trades/$T/orders" \
    -H "Authorization: Bearer $OANDA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"takeProfit\":{\"price\":\"$TP\"},\"stopLoss\":{\"price\":\"$SL\"}}" >/dev/null
done
log_event "Initial TP=$TP, SL=$SL applied to trades: $TRADE_IDS"

# 2) Trailing loop
while true; do
  BID=$(curl -sS -H "Authorization: Bearer $OANDA_API_KEY" \
    "https://$HOST/v3/accounts/$ACCOUNT_ID/pricing?instruments=$PAIR" \
    | jq -r '.prices[0].bids[0].price')

  if [ -z "$BID" ] || [ "$BID" = "null" ]; then sleep 5; continue; fi

  # Trail SL upward
  if (( $(echo "$BID > $SL + $STEP" | bc -l) )); then
    SL_NEW=$(printf "%.5f" "$(echo "$BID - $BUFFER" | bc -l)")
    for T in $TRADE_IDS; do
      curl -sS -X PUT "https://$HOST/v3/accounts/$ACCOUNT_ID/trades/$T/orders" \
        -H "Authorization: Bearer $OANDA_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"takeProfit\":{\"price\":\"$TP\"},\"stopLoss\":{\"price\":\"$SL_NEW\"}}" >/dev/null
    done
    log_event "SL updated from $SL -> $SL_NEW (BID=$BID)"
    SL="$SL_NEW"
  fi

  # Bump TP to 1.1700 if 1.1680 breaks
  if (( $(echo "$BID >= 1.1680" | bc -l) )) && (( $(echo "$TP < 1.1700" | bc -l) )); then
    TP_NEW=1.1700
    for T in $TRADE_IDS; do
      curl -sS -X PUT "https://$HOST/v3/accounts/$ACCOUNT_ID/trades/$T/orders" \
        -H "Authorization: Bearer $OANDA_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"takeProfit\":{\"price\":\"$TP_NEW\"},\"stopLoss\":{\"price\":\"$SL\"}}" >/dev/null
    done
    log_event "🚀 TP bumped from $TP -> $TP_NEW (BID=$BID)"
    TP="$TP_NEW"
  fi

  sleep 10
done
