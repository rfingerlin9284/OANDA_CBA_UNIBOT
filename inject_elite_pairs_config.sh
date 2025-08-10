#!/bin/bash

echo "📦 Updating live_config.json with 18+18 optimized pairs..."

CONFIG_FILE=$(find . -type f -name "live_config.json" | head -n 1)

if [ -z "$CONFIG_FILE" ]; then
  echo "❌ live_config.json not found."
  exit 1
fi

cp "$CONFIG_FILE" "$CONFIG_FILE.bak"
echo "📁 Backup created at $CONFIG_FILE.bak"

jq '.pairs = {
  "forex": [
    "EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF", "AUD/USD", "NZD/USD",
    "EUR/JPY", "GBP/JPY", "EUR/GBP", "USD/CAD", "EUR/CHF", "AUD/JPY",
    "CHF/JPY", "GBP/CHF", "NZD/JPY", "CAD/JPY", "EUR/AUD", "GBP/AUD"
  ],
  "crypto": [
    "BTC/USD", "ETH/USD", "SOL/USD", "DOGE/USD", "XRP/USD", "ADA/USD",
    "AVAX/USD", "LINK/USD", "MATIC/USD", "DOT/USD", "LTC/USD", "APT/USD",
    "BCH/USD", "UNI/USD", "OP/USD", "NEAR/USD", "INJ/USD", "XLM/USD"
  ]
}' "$CONFIG_FILE.bak" > "$CONFIG_FILE"

echo "✅ Updated live_config.json with elite 18 forex + 18 crypto pairs."
