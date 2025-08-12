#!/usr/bin/env bash
set -euo pipefail
source .env.live
echo "🔍 Checking OANDA account summary..."
curl -sS -H "Authorization: Bearer $OANDA_API_TOKEN" \
  "$OANDA_API_URL/v3/accounts/$OANDA_ACCOUNT_ID/summary" | jq .
echo "🔍 Coinbase server time..."
curl -sS "$CB_API_URL/api/v3/brokerage/market/products" | jq '.num_products?'
