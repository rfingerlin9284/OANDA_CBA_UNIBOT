#!/bin/bash

# Auto-detect live config JSON
CONFIG_FILE=$(find . -type f -name "live_config.json" | head -n 1)

if [ -z "$CONFIG_FILE" ]; then
  echo "❌ live_config.json not found anywhere inside this folder."
  exit 1
fi

echo "🧰 Fixing config file: $CONFIG_FILE"

# Backup
cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
echo "📦 Backup saved as: ${CONFIG_FILE}.bak"

# Inject 'pairs' key if missing
if ! grep -q '"pairs"' "$CONFIG_FILE"; then
  jq '. + { "pairs": { "forex": ["EUR/USD", "USD/JPY"], "crypto": ["BTC/USD", "ETH/USD"] } }' "$CONFIG_FILE" > tmp.json && mv tmp.json "$CONFIG_FILE"
  echo "✅ 'pairs' key injected with default values"
else
  echo "✅ 'pairs' key already exists - no changes made"
fi

echo "✅ Patch complete. Swarm should now boot clean."
