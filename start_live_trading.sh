#!/bin/bash
# 🚀 WOLFPACK LIVE TRADING STARTUP SCRIPT
# Constitutional PIN: 841921
# LIVE TRADING ONLY - NO SIMULATION MODE

echo "🚀 WOLFPACK-LITE LIVE TRADING STARTUP"
echo "Constitutional PIN: 841921"
echo "=" * 60
echo "🚨 LIVE TRADING ONLY - REAL MONEY AT RISK"
echo "🛡️  ALL SIMULATION MODES ELIMINATED"
echo "=" * 60

# Enforce live mode
python3 enforce_live_mode.py

# Verify environment
echo ""
echo "🔍 VERIFYING LIVE-ONLY CONFIGURATION..."

# Check .env file
if grep -q "OANDA_ENVIRONMENT=live" .env; then
    echo "✅ .env: OANDA environment set to live"
else
    echo "❌ .env: OANDA environment not set to live"
    exit 1
fi

if grep -q "SIM_MODE=false" .env; then
    echo "✅ .env: SIM_MODE disabled"
else
    echo "❌ .env: SIM_MODE not properly disabled"
    exit 1
fi

if grep -q "PRACTICE=false" .env; then
    echo "✅ .env: PRACTICE mode disabled"
else
    echo "❌ .env: PRACTICE mode not properly disabled"
    exit 1
fi

# Check config.py
if grep -q 'OANDA_ENVIRONMENT = "live"' config.py; then
    echo "✅ config.py: OANDA environment set to live"
else
    echo "❌ config.py: OANDA environment not set to live"
    exit 1
fi

if grep -q "SIM_MODE = False" config.py; then
    echo "✅ config.py: SIM_MODE disabled"
else
    echo "❌ config.py: SIM_MODE not properly disabled"
    exit 1
fi

# Verify no practice endpoints
if grep -q "api-fxpractice" .env config.py credentials.py 2>/dev/null; then
    echo "❌ PRACTICE endpoints detected - ABORTING"
    exit 1
else
    echo "✅ No practice endpoints found"
fi

# Check for required live endpoint
if grep -q "api-fxtrade.oanda.com" .env; then
    echo "✅ OANDA live endpoint confirmed"
else
    echo "❌ OANDA live endpoint not found"
    exit 1
fi

echo ""
echo "🎯 PRE-FLIGHT CHECK RESULTS:"
echo "✅ Environment: LIVE ONLY"
echo "✅ Endpoints: LIVE ONLY" 
echo "✅ Configuration: LIVE ONLY"
echo "✅ Simulation modes: ELIMINATED"
echo ""

echo "🚨 FINAL WARNING: This system will trade with REAL MONEY"
echo "💰 OANDA Live Account: 001-001-13473069-001"
echo "🔐 Constitutional PIN: 841921"
echo ""

read -p "Type 'START LIVE TRADING' to launch: " confirm

if [ "$confirm" != "START LIVE TRADING" ]; then
    echo "❌ Live trading not confirmed - startup cancelled"
    exit 0
fi

echo ""
echo "🚀 LAUNCHING LIVE TRADING SYSTEM..."
echo "🔴 REAL MONEY MODE ACTIVE"
echo ""

# Launch the live trading system
python3 live_trading_main.py
