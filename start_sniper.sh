#!/bin/bash

# WOLFPACK-LITE SNIPER LAUNCHER
# LIVE TRADING ONLY - REAL MONEY AT RISK
# NO DEMO/PRACTICE/SANDBOX MODE

echo "=================================================="
echo "🐺 WOLFPACK-LITE FVG SNIPER LAUNCHER"
echo "🚨 LIVE TRADING MODE - REAL MONEY AT RISK!"
echo "💰 SPOT MARKETS ONLY - NO PERPS/MARGIN"
echo "=================================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected!"
    echo "💡 Run: source venv/bin/activate"
    exit 1
fi

# Check if required files exist
required_files=("fvg_strategy.py" "oanda_sniper.py" "coinbase_sniper.py" "executor.py" "credentials.py" "logger.py")

for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

echo "✅ All required files present"

# Check Python dependencies
echo "🔍 Checking dependencies..."
python -c "import oandapyV20, ccxt, numpy, pandas, talib" 2>/dev/null
if [[ $? -ne 0 ]]; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

echo "✅ Dependencies verified"

# Create logs directory if it doesn't exist
mkdir -p logs

# Show configuration
echo ""
echo "📊 CONFIGURATION:"
echo "   • OANDA: 12 forex pairs (EUR/USD, GBP/USD, etc.)"
echo "   • Coinbase: 8 spot crypto pairs (BTC/USD, ETH/USD, etc.)"
echo "   • Strategy: FVG + Fibonacci + RSI confluence"
echo "   • Risk: 1% per trade with 1:3 R:R minimum"
echo "   • OCO: Mandatory stop-loss and take-profit"
echo "   • Max: 1 trade per pair (no doubling down)"
echo ""

# Confirm live trading
echo "🚨 WARNING: This will trade with REAL MONEY!"
echo "🚨 Make sure your API keys are correctly configured!"
echo ""
read -p "🤔 Are you sure you want to start LIVE trading? (yes/no): " confirm

if [[ $confirm != "yes" ]]; then
    echo "❌ Trading cancelled by user"
    exit 0
fi

echo ""
echo "🚀 Starting FVG snipers..."
echo "📊 OANDA forex sniper starting in 3 seconds..."
sleep 3

# Start OANDA sniper in background
python oanda_sniper.py &
OANDA_PID=$!
echo "✅ OANDA sniper started (PID: $OANDA_PID)"

sleep 2

echo "📊 Coinbase spot sniper starting in 3 seconds..."
sleep 3

# Start Coinbase sniper in background  
python coinbase_sniper.py &
COINBASE_PID=$!
echo "✅ Coinbase sniper started (PID: $COINBASE_PID)"

echo ""
echo "=================================================="
echo "🐺 BOTH SNIPERS ACTIVE - LIVE TRADING!"
echo "🚨 REAL MONEY AT RISK!"
echo "=================================================="
echo "📊 OANDA Forex PID: $OANDA_PID"
echo "📊 Coinbase Spot PID: $COINBASE_PID"
echo ""
echo "🛑 To stop both snipers: Ctrl+C or kill $OANDA_PID $COINBASE_PID"
echo ""

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all snipers..."
    kill $OANDA_PID 2>/dev/null
    kill $COINBASE_PID 2>/dev/null
    echo "✅ All snipers stopped"
    exit 0
}

# Trap Ctrl+C to cleanup
trap cleanup SIGINT

# Wait for both processes
wait $OANDA_PID $COINBASE_PID

echo "🐺 All snipers have stopped"
