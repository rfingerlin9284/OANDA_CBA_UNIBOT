#!/bin/bash

# 🎯 WOLFPACK-LITE DASHBOARD LAUNCHER
# Launch FVG monitoring dashboards for live trading

echo "🎯 WOLFPACK-LITE FVG DASHBOARD LAUNCHER"
echo "🚨 LIVE TRADING MONITORING - REAL MONEY AT RISK"
echo "=============================================="

# Check if rich is installed
python -c "import rich" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Rich library not found. Installing..."
    pip install rich>=13.0.0
fi

echo ""
echo "Available dashboards:"
echo "1. OANDA Forex FVG Dashboard"
echo "2. Coinbase Spot Crypto FVG Dashboard"
echo "3. Launch both dashboards (split terminal)"
echo ""

read -p "Select dashboard (1-3): " choice

case $choice in
    1)
        echo "🚀 Launching OANDA FVG Dashboard..."
        echo "🚨 WARNING: LIVE FOREX TRADING MONITORING"
        python dashboards/oanda_fvg_cli.py
        ;;
    2)
        echo "🚀 Launching Coinbase Spot FVG Dashboard..."
        echo "🚨 WARNING: LIVE CRYPTO SPOT TRADING MONITORING"
        python dashboards/coinbase_fvg_cli.py
        ;;
    3)
        echo "🚀 Launching both dashboards..."
        echo "🚨 WARNING: LIVE TRADING MONITORING FOR BOTH PLATFORMS"
        echo "Opening in split terminal..."
        
        # Try to use tmux if available
        if command -v tmux &> /dev/null; then
            tmux new-session -d -s wolfpack_dashboards \; \
                split-window -h \; \
                send-keys -t 0 'python dashboards/oanda_fvg_cli.py' Enter \; \
                send-keys -t 1 'python dashboards/coinbase_fvg_cli.py' Enter \; \
                attach-session -t wolfpack_dashboards
        else
            echo "❌ tmux not found. Install tmux for split screen or run dashboards separately."
            echo "Starting OANDA dashboard (press Ctrl+C to switch to Coinbase)"
            python dashboards/oanda_fvg_cli.py
        fi
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "✅ Dashboard session ended."
