#!/bin/bash
# oanda_status.sh — JSON + color-coded human-readable status
set -euo pipefail

KEY="${OANDA_LIVE_API_KEY}"
ACC="001-001-13473069-001"
HOST="api-fxtrade.oanda.com"
PAIR="EUR_USD"

# Colors (disable if not a TTY)
if [ -t 1 ]; then RED=$'\033[31m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RESET=$'\033[0m'
else RED=""; GREEN=""; YELLOW=""; RESET=""
fi

echo "============================================"
echo -e "📡 Checking OANDA Status for ${YELLOW}${PAIR}${RESET}"
echo "============================================"

# --- Position (RAW) ---
POS_JSON=$(curl -sS -H "Authorization: Bearer $KEY" "https://$HOST/v3/accounts/$ACC/positions/$PAIR" || echo '{}')
echo ""
echo "🔹 Open Position (RAW JSON):"
echo "$POS_JSON" | jq '{units:.position.long.units, entry:.position.long.averagePrice}'

# --- Position (HUMAN) ---
POS_UNITS=$(echo "$POS_JSON" | jq -r '.position.long.units // "0"' 2>/dev/null || echo "0")
POS_ENTRY=$(echo "$POS_JSON" | jq -r '.position.long.averagePrice // ""' 2>/dev/null || echo "")
if [[ "$POS_UNITS" != "0" && -n "$POS_ENTRY" ]]; then
  echo -e "🔹 Open Position (HUMAN READABLE):"
  echo -e "   ${PAIR} — ${YELLOW}${POS_UNITS} units${RESET} @ ${YELLOW}${POS_ENTRY}${RESET}"
else
  echo "🔹 No open long position on $PAIR."
fi

# --- Pending orders (RAW) ---
ORDERS_JSON=$(curl -sS -H "Authorization: Bearer $KEY" "https://$HOST/v3/accounts/$ACC/pendingOrders" || echo '{"orders":[]}')
echo ""
echo "📋 Pending Orders (RAW JSON):"
echo "$ORDERS_JSON" | jq '.orders | map({id,type,price,units,tag:(.clientExtensions.tag // null)})'

# --- Pending orders (HUMAN + COLORS) ---
echo "📋 Pending Orders (HUMAN READABLE):"
echo "$ORDERS_JSON" \
| jq -r '.orders[]? | @tsv "\(.type)\t\(.price)\t\(.units)\t\((.clientExtensions.tag // "—"))"' \
| while IFS=$'\t' read -r TYP PRICE UNITS TAG; do
    case "$TYP" in
      STOP)  echo -e "   ${RED}STOP  @ ${PRICE} for ${UNITS} units [Tag: ${TAG}]${RESET}" ;;
      LIMIT) echo -e "   ${GREEN}LIMIT @ ${PRICE} for ${UNITS} units [Tag: ${TAG}]${RESET}" ;;
      *)     echo -e "   ${TYP} @ ${PRICE} for ${UNITS} units [Tag: ${TAG}]" ;;
    esac
  done

echo "============================================"
