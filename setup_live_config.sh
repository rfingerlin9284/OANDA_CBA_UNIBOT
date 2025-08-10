#!/bin/bash
# 🔧 Full config patcher — uses full 12-pair model & correct paths

mkdir -p config

cat << 'CONFIG' > config/live_config.json
{
  "mode": "live",
  "api_keys": {
    "oanda": "5f2cd72673e5c6214f94cc159e444a01-c229936202d1b6d0b4499086198da2b3",
    "coinbase": "2636c881-b44e-4263-b05d-fb10a5ad1836"
  },
  "pairs": {
    "forex": [
      "EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF",
      "AUD/USD", "NZD/USD"
    ],
    "crypto": [
      "BTC/USD", "ETH/USD", "SOL/USD", "DOGE/USD",
      "XRP/USD", "ADA/USD"
    ]
  },
  "risk_settings": {
    "max_leverage": 1.5,
    "stop_loss_pct": 1.5,
    "take_profit_pct": 3.0
  },
  "strategy": "GoldenZoneFVG",
  "ml_model_path": "models/wolfpack_ml_12pair.pkl",
  "constitutional_pin_required": true
}
CONFIG

echo "✅ live_config.json written with 12 pairs + correct model path"
