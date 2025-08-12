#!/usr/bin/env bash
set -euo pipefail

KEY="${OANDA_LIVE_API_KEY}"
ACC='001-001-13473069-001'
HOST='api-fxtrade.oanda.com'
PAIR='EUR_USD'
TAG='RBOTzilla_FORCE_OCO'
LOG='oco_watchdog.log'

# Ensure jq exists
command -v jq >/dev/null || { sudo apt-get update -y && sudo apt-get install -y jq; }

log(){ echo "$(date '+%Y-%m-%d %H:%M:%S')  $*" | tee -a "$LOG"; }

log "🚀 Watchdog started for $PAIR (tag=$TAG)..."

while true; do
    sleep 3
    POS=$(curl -sS -H "Authorization: Bearer $KEY" \
        "https://$HOST/v3/accounts/$ACC/positions/$PAIR" \
        | jq -r '.position.long.units // "0"' 2>/dev/null || echo "0")

    if [ "$POS" = "0" ] || [ "$POS" = "0.0000" ]; then
        log "💡 Position closed. Canceling remaining tagged OCO orders..."
        curl -sS -H "Authorization: Bearer $KEY" \
            "https://$HOST/v3/accounts/$ACC/pendingOrders" \
            | jq -r --arg tag "$TAG" '.orders // [] | map(select(.clientExtensions?.tag==$tag) | .id) | .[]' \
            | while read -r OID; do
                [ -z "$OID" ] && continue
                curl -sS -X PUT -H "Authorization: Bearer $KEY" \
                    "https://$HOST/v3/accounts/$ACC/orders/$OID/cancel" >/dev/null || true
                log "❌ Canceled order $OID"
            done
        log "✅ All tagged orders cleared. Watchdog exiting."
        exit 0
    fi
done
