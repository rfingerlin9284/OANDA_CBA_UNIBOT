#!/usr/bin/env python3
"""
🎯 WOLFPACK SNIPER v2.0 - EXACT HARDCODED VALUES
Aggressive FVG Hunter with Mandatory OCO + Smart Trailing
"""

# ========== 1. ENTRY CONFLUENCE RULES ==========
ENTRY_RULES = {
    # Rule 1.1: Valid FVG Gap Size
    'MIN_FVG_GAP_PCT': 0.15,  # 0.15% of price minimum
    
    # Rule 1.2: Fibonacci Golden Zone 
    'FIB_ENTRY_MIN': 61.8,    # 61.8% retracement minimum
    'FIB_ENTRY_MAX': 65.0,    # 65.0% retracement maximum
    
    # Rule 1.3: RSI Direction Confirmation
    'RSI_LONG_MIN': 60,       # RSI > 60 for longs
    'RSI_SHORT_MAX': 40,      # RSI < 40 for shorts
    'RSI_PERIOD': 14,         # Standard 14-period RSI
    
    # Rule 1.4: EMA Trend Filter
    'EMA_FAST': 20,           # EMA20 for trend
    'EMA_SLOW': 50,           # EMA50 for trend
    
    # Optional: Volume Spike Filter
    'VOLUME_SPIKE_MULTIPLIER': 1.5,  # 1.5x average volume
    'VOLUME_LOOKBACK': 20,    # 20-period average
}

# ========== 2. RISK CONTROL (EXACT VALUES) ==========
RISK_CONFIG = {
    'BASE_CAPITAL': 3000,     # Starting capital
    'RISK_PER_TRADE_PCT': 1.0,  # 1% risk per trade
    'MAX_RISK_PER_TRADE_PCT': 1.5,  # 1.5% max (with scaling)
    'MAX_TRADES_PER_DAY': 10, # Maximum 10 trades/day
    'MIN_RR_RATIO': 2.5,      # Minimum 1:2.5 risk/reward
    'TARGET_RR_RATIO': 3.0,   # Target 1:3 risk/reward
}

# ========== 3. OCO + SMART TRAILING ==========
OCO_CONFIG = {
    'MANDATORY_OCO': True,    # Every trade MUST have OCO
    'OCO_TIMEOUT_SEC': 5,     # 5 seconds to confirm OCO
    'TRAIL_TRIGGER_R': 2.0,   # Start trailing at +2R
    'TRAIL_LOCK_R': 1.0,      # Lock in +1R when trailing
    'TRAIL_STEP_PIPS': 5,     # Trail in 5-pip steps
}

# ========== 4. POSITION SCALING (STREAK LOGIC) ==========
SCALING_CONFIG = {
    'WIN_STREAK_3_BONUS': 1.25,  # +25% size after 3 wins
    'WIN_STREAK_5_BONUS': 1.40,  # +40% size after 5 wins
    'LOSE_STREAK_2_PENALTY': 0.50,  # -50% size after 2 losses
    'RESET_AFTER_LOSS': True,    # Reset to base after any loss
    'MAX_POSITION_MULTIPLIER': 2.0,  # Never exceed 2x base size
}

# ========== 5. PAIRS & TIMEFRAMES ==========
TRADING_PAIRS = {
    'COINBASE': [
        'BTC/USD', 'ETH/USD', 'SOL/USD', 'AVAX/USD', 'MATIC/USD',
        'LINK/USD', 'UNI/USD', 'AAVE/USD', 'DOT/USD', 'ADA/USD'
    ],
    'OANDA': [
        'EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CAD',
        'USD_CHF', 'NZD_USD', 'EUR_GBP', 'EUR_JPY', 'GBP_JPY'
    ]
}

TIMEFRAMES = {
    'PRIMARY': '5m',    # 5-minute for entry signals
    'TREND': '15m',     # 15-minute for trend confirmation
    'CANDLE_LIMIT': 100, # 100 candles for analysis
}

# ========== 6. TERMINAL OUTPUT CONFIG ==========
TERMINAL_CONFIG = {
    'SHOW_PNL': True,         # Show running P&L
    'SHOW_BALANCE': True,     # Show account balance
    'SHOW_STREAK': True,      # Show win/loss streak
    'LOG_TO_FILE': True,      # Save to trade_log.txt
    'REFRESH_RATE_SEC': 10,   # Update every 10 seconds
}

# ========== 7. WEEKLY ADAPTATION ==========
ADAPTATION_CONFIG = {
    'REVIEW_DAYS': 7,         # Review every 7 days
    'AUTO_ADJUST_SIZE': True, # Auto-adjust position sizing
    'WIN_RATE_TARGET': 40,    # Target 40% win rate
    'DAILY_TARGET_USD': 400,  # $400/day target
}

# ========== TARGET PERFORMANCE ==========
PERFORMANCE_TARGETS = {
    'DAILY_PROFIT_TARGET': 400,  # $400/day
    'MONTHLY_TARGET': 8000,      # $8k/month  
    'DAILY_ROI_TARGET': 8.0,     # 8% daily ROI (from $5k)
    'MAX_DAILY_LOSS': -200,      # Max $200 daily loss
}

# ========== SHARP SNIPER WEIGHT SYSTEM ==========
WEIGHT_SYSTEM = {
    'BASE_WEIGHT': 1.0,
    'FIB_BONUS': 1.0,           # +1.0 for fibonacci zone
    'RSI_BONUS': 0.5,           # +0.5 for RSI confirmation  
    'EMA_BONUS': 0.5,           # +0.5 for EMA trend
    'VOLUME_BONUS': 1.0,        # +1.0 for volume spike
    'MIN_WEIGHT_THRESHOLD': 1.5, # Need 1.5+ to enter
    'HIGH_CONFIDENCE_THRESHOLD': 3.0, # 3.0+ = high confidence
}

# ========== API SETTINGS ==========
API_CONFIG = {
    'MAX_RETRIES': 3,
    'RETRY_DELAY_SEC': 2,
    'RATE_LIMIT_DELAY': 0.5,
    'HEARTBEAT_INTERVAL': 30,
}

print("🎯 SNIPER CONFIG LOADED - Ready for predator mode")
