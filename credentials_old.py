#!/usr/bin/env python3
"""
🔐 WOLFPACK-LITE CREDENTIALS
LIVE API KEYS - NEVER COMMIT TO GIT!
Replace with your actual keys before running.
"""

class WolfpackCredentials:
    """🔐 CENTRALIZED CREDENTIALS MANAGER"""
    
    def __init__(self):
        print("🔐 Credentials loaded - Ready for live trading")
        
    # ========== OANDA LIVE CREDENTIALS ==========
    OANDA_API_KEY = "PASTE_YOUR_OANDA_API_TOKEN_HERE"
    OANDA_ACCOUNT_ID = "PASTE_YOUR_OANDA_ACCOUNT_ID_HERE"
    
    # ========== COINBASE PRO CREDENTIALS ==========
    COINBASE_API_KEY = "PASTE_YOUR_COINBASE_API_KEY_HERE"
    COINBASE_SECRET = "PASTE_YOUR_COINBASE_SECRET_HERE"
    COINBASE_PASSPHRASE = "PASTE_YOUR_COINBASE_PASSPHRASE_HERE"
    live_mode = True  # Change to False for real money
    
    # ========== BOT CONFIGURATION ==========
    # Capital & Risk Settings
STARTING_CAPITAL = 3000  # Starting balance
RISK_PER_TRADE = 0.01   # 1% risk per trade
MAX_TRADES_PER_DAY = 10
MAX_CONCURRENT_TRADES = 3

# Trading Pairs
FOREX_PAIRS = [
    "EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD",
    "USD_CHF", "NZD_USD", "EUR_GBP", "EUR_JPY", "GBP_JPY"
]

CRYPTO_PAIRS = [
    "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "XRP-USD",
    "DOGE-USD", "AVAX-USD", "DOT-USD", "MATIC-USD", "LINK-USD"
]

# ========== SNIPER SETTINGS ==========
# FVG Detection
MIN_GAP_PERCENT = 0.15  # Minimum gap size as % of price
MAX_FVG_AGE = 5        # Expire FVG after 5 candles

# Risk Reward
MIN_RR_RATIO = 2.5     # Minimum 1:2.5 risk reward
TARGET_RR_RATIO = 3.0  # Target 1:3 risk reward

# Confluence Requirements
RSI_BULL_MIN = 60      # RSI > 60 for bullish bias
RSI_BEAR_MAX = 40      # RSI < 40 for bearish bias

# Position Scaling (Streak Logic)
STREAK_SCALE_UP = {3: 1.25, 5: 1.4}    # Win streak multipliers
STREAK_SCALE_DOWN = {2: 0.5}            # Loss streak reduction

print("🔐 Credentials loaded - Ready for live trading")
