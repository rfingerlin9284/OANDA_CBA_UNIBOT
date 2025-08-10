#!/bin/bash

# 🚀 WOLFPACK-PROTO DEPLOYMENT GUIDE
# Enhanced autonomous trading system with mass psychology quantification

set -euo pipefail

echo "🌟 WOLFPACK-PROTO: Enhanced Autonomous Trading Bot"
echo "================================================================"
echo "🧠 Mass Psychology Quantifier Edition"
echo "⚡ Dynamic OCO Wave Riders | Bias-Aware Dispatch | Lock Mode"
echo "🌍 Hamilton, NJ Timezone | Session-Aware Trading"
echo "🔥 Live Trading Only - Real Money, Real Results"
echo "================================================================"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the wolfpack-lite directory"
    exit 1
fi

# Validate credentials
echo "🔐 Validating credentials..."
python3 -c "
from credentials import WolfpackCredentials
creds = WolfpackCredentials()
issues = creds.validate_credentials()
if issues:
    print('❌ Credential issues found:')
    for issue in issues:
        print(f'   - {issue}')
    print()
    print('🔧 Please edit credentials.py to fix these issues')
    exit(1)
else:
    print('✅ All credentials properly configured')
    summary = creds.get_trading_summary()
    print(f'📊 System Config: {summary[\"total_pairs\"]} pairs, {summary[\"risk_per_trade\"]} risk')
    print(f'🔥 Wave Ride: {summary[\"wave_ride_threshold\"]} threshold, {summary[\"trail_percent\"]} trail')
"

if [ $? -ne 0 ]; then
    echo "❌ Credential validation failed. Please fix issues above."
    exit 1
fi

# Create necessary directories
mkdir -p logs dashboards/feeds data/coinbase data/oanda

echo ""
echo "🚀 WOLFPACK-PROTO FEATURES:"
echo "   ✅ Enhanced FVG detection with mass psychology quantification"
echo "   ✅ Dynamic OCO wave riders (remove TP caps on momentum)"
echo "   ✅ Market-aware scoring (crypto momentum vs forex reversion)"
echo "   ✅ Bull/bear bias dispatch (session-aware SL adjustments)"
echo "   ✅ Volume surge filters for crypto edges"
echo "   ✅ Lock mode for ultra-R signals (3.0+ RR pure trail)"
echo "   ✅ Gap size weighting for psychological urgency"
echo "   ✅ OCO watchdog auto-kills orphans"
echo "   ✅ Heartbeat visuals and guardian monitoring"
echo "   ✅ Arbitrage engine for 24/7 cross-platform edges"
echo ""

# Check if user wants to start
read -p "🎯 Ready to start hunting? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🏹 Starting Wolfpack-Proto system..."
    echo "📊 Monitor logs: tail -f logs/trade_log.txt"
    echo "🛑 Emergency stop: Ctrl+C or killall python3"
    echo ""
    
    # Start the system
    python3 main.py
else
    echo "🛑 Launch cancelled by user"
    echo ""
    echo "📘 Manual start: python3 main.py"
    echo "📊 Check logs: tail -f logs/trade_log.txt"
    echo "🔧 Edit config: nano credentials.py"
fi

echo ""
echo "📚 Documentation:"
echo "   - README.md: Complete system overview"
echo "   - COMPLETE_SYSTEM_AUDIT.md: Detailed technical analysis"
echo "   - DETAILED_PERFORMANCE_ANALYSIS.md: Performance metrics"
echo "   - credentials.py: Configuration and parameters"
echo ""
echo "⚠️  LIVE TRADING WARNING:"
echo "   This system trades with real money on live accounts"
echo "   Monitor performance closely"
