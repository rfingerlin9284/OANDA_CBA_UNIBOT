#!/bin/bash
# 💓 WOLFPACK-LITE HEARTBEAT MONITOR
# Checks system health every 20 seconds

HEARTBEAT_LOG="logs/health/heartbeat.log"
CONFIG_FILE="config.json"

# Create logs/health directory if it doesn't exist
mkdir -p logs/health

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Check if config.json exists and get mode
    if [ -f "$CONFIG_FILE" ]; then
        MODE=$(grep -o '"mode":[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
    else
        MODE="unknown"
    fi
    
    # Check if ML models exist
        ML_STATUS="✅ ML_LOADED"
    else
        ML_STATUS="❌ ML_MISSING"
    fi
    
        BACKTEST_STATUS="🔄 BACKTEST_ACTIVE"
    else
        BACKTEST_STATUS="⏸️ BACKTEST_IDLE"
    fi
    
    # Generate heartbeat message - LIVE TRADING ONLY
    HEART_MSG="💓 LIVE MODE ACTIVE – REAL TRADING ENABLED"
    STATUS_COLOR="🔴"
    
    # Log heartbeat
    echo "[$TIMESTAMP] $STATUS_COLOR $HEART_MSG | $ML_STATUS | $BACKTEST_STATUS" >> "$HEARTBEAT_LOG"
    
    # Keep only last 100 heartbeat entries
    tail -100 "$HEARTBEAT_LOG" > "${HEARTBEAT_LOG}.tmp" && mv "${HEARTBEAT_LOG}.tmp" "$HEARTBEAT_LOG"
    
    sleep 20
done
