#!/bin/bash

echo "🔐 Constitutional PIN: 841921"
echo "🕒 Started: $(date -u)"
echo ""

# Activate trading environment
ENV_PATH="./coinbase_env/bin/activate"
if [ -f "$ENV_PATH" ]; then
  source "$ENV_PATH"
  echo "✅ Virtual environment activated"
else
  echo "⚠️ Environment not found at $ENV_PATH, proceeding with system Python"
fi

# Check for models (create fallbacks if missing)

# Create models directory if it doesn't exist
mkdir -p models

# Create fallback models if they don't exist
if [[ ! -f "$FOREX_MODEL" ]]; then
  echo "⚠️ Creating fallback forex model at $FOREX_MODEL"
  cp models/oanda_ml.pkl "$FOREX_MODEL" 2>/dev/null || echo "📝 Will use liveulator for forex model"
fi

if [[ ! -f "$CRYPTO_MODEL" ]]; then
  echo "⚠️ Creating fallback crypto model at $CRYPTO_MODEL" 
  cp models/crypto_ml.pkl "$CRYPTO_MODEL" 2>/dev/null || echo "📝 Will use liveulator for crypto model"
fi

# Create config directory and default config if needed
mkdir -p config logs

if [[ ! -f "config/live_config.json" ]]; then
  echo "📝 Creating default config file..."
  cat > config/live_config.json << 'EOF'
{
  "risk_per_trade": 0.02,
  "confidence_threshold": 0.72,
  "stop_loss": 0.015,
  "take_profit": 0.025,
  "max_daily_trades": 12,
  "max_concurrent_positions": 6,
  "pairs": {
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
  }
}
EOF
fi

LOOKBACK_DAYS=90
INITIAL_CAPITAL=5000
LEVERAGE=1.5

echo "🎯 BACKTEST CONFIGURATION:"
echo "   📅 Lookback Period: $LOOKBACK_DAYS days"
echo "   💰 Initial Capital: \$$INITIAL_CAPITAL"
echo "   📈 Leverage: ${LEVERAGE}x"
echo "   📊 Log File: $LOG_PATH"
echo "   🏆 Total Pairs: 36 (18 Forex + 18 Crypto)"
echo ""
echo ""

  --mode dual \
  --forex-model "$FOREX_MODEL" \
  --crypto-model "$CRYPTO_MODEL" \
  --config config/live_config.json \
  --lookback-days $LOOKBACK_DAYS \
  --capital $INITIAL_CAPITAL \
  --leverage $LEVERAGE \
  --log-path "$LOG_PATH"

if [ $? -eq 0 ]; then
  echo ""
  echo ""
  echo "📊 QUICK RESULTS SUMMARY:"
  echo "════════════════════════════════════════════════════════════"
  
  # Extract key results from log file
  if [ -f "$LOG_PATH" ]; then
    echo "📁 Full results saved to: $LOG_PATH"
    echo ""
    echo "────────────────────────────────────────────────────────────"
    tail -15 "$LOG_PATH" | grep -E "(Balance|P/L|ROI|Win Rate|Drawdown|Performance Grade)" | head -10
    echo "────────────────────────────────────────────────────────────"
    echo ""
    echo "📖 VIEWING OPTIONS:"
    echo "   tail -f $LOG_PATH           # Follow live updates"
    echo "   tail -50 $LOG_PATH          # View last 50 lines"
    echo "   grep 'WIN\\|LOSS' $LOG_PATH | tail -20  # Last 20 trades"
    echo ""
  else
    echo "⚠️ Log file not found at $LOG_PATH"
  fi
else
  exit 1
fi

echo ""
echo "🔐 Constitutional PIN: 841921 - Elite Squad Battle Tested!"
