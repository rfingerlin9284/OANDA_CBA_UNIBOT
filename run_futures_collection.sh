#!/usr/bin/env bash
# run_futures_collection.sh
# Complete futures data collection and signal generation pipeline

set -euo pipefail

echo "🚀 HIVE MIND RICK - FUTURES DATA PIPELINE"
echo "=========================================="
echo "🎯 Collecting Coinbase futures + CryptoPanic sentiment"
echo "🔥 Generating trading signals with enhanced intelligence"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Create data directories
mkdir -p data/futures data/cryptopanic

echo "📊 Step 1: Collecting futures data from Coinbase free API..."
python3 coinbase_futures_collector.py

echo ""
echo "🎯 Step 2: Generating enhanced trading signals..."
python3 futures_signal_engine.py

echo ""
echo "✅ PIPELINE COMPLETE!"
echo "📁 Check data/ directory for collected data and signals"
echo "🎉 Ready for HIVE MIND RICK integration!"
