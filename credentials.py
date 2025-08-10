#!/usr/bin/env python3
"""
🔐 WOLFPACK-LITE CREDENTIALS - RBOTZILLA UPGRADED
Constitutional PIN: 841921
LIVE TRADING ONLY - REAL MONEY AT RISK
"""

import os

class WolfpackCredentials:
    """🔐 CENTRALIZED CREDENTIALS MANAGER - LIVE TRADING ONLY - RBOTZILLA ENHANCED"""
    
    def __init__(self):
        print("🔐 RBOTZILLA ENHANCED LIVE TRADING CREDENTIALS LOADED")
        
    # ========== CONSTITUTIONAL SECURITY ==========
    CONSTITUTIONAL_PIN = "841921"
    
    # ========== OANDA LIVE CREDENTIALS ==========
    OANDA_API_KEY = "9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
    OANDA_ACCOUNT_ID = "001-001-13473069-001"
    OANDA_ENVIRONMENT = "live"  # LIVE TRADING ONLY
    OANDA_LIVE_URL = "https://api-fxtrade.oanda.com"  # LIVE ENDPOINT

def get_oanda_credentials():
    """Get OANDA credentials for FVG strategy"""
    creds = WolfpackCredentials()
    return {
        'access_token': creds.OANDA_API_KEY,
        'account_id': creds.OANDA_ACCOUNT_ID,
        'environment': creds.OANDA_ENVIRONMENT,
        'api_url': creds.OANDA_LIVE_URL
    }
    
    # ========== COINBASE ADVANCED TRADE LIVE CREDENTIALS - RBOTZILLA FIXED ==========
    COINBASE_API_KEY_ID = "2636c881-b44e-4263-b05d-fb10a5ad1836"  # Hard-coded live
    COINBASE_PRIVATE_KEY = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="  # 64-byte full key
    
    # RBOTZILLA ENHANCED: Load fixed PEM file
    @property
    def COINBASE_PRIVATE_KEY_PEM(self):
        """Load the surgically repaired PEM file"""
        try:
            with open('coinbase_private_fixed.pem', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback to inline PEM creation
            return self._create_inline_pem()
    
    def _create_inline_pem(self):
        """Fallback inline PEM creation if file missing"""
        import base64
        
        # Extract 32-byte seed from full key
        full_key = base64.b64decode(self.COINBASE_PRIVATE_KEY)
        seed_32_bytes = full_key[:32]
        
        # Create PKCS#8 structure
        pkcs8_prefix = bytes([
            0x30, 0x2e, 0x02, 0x01, 0x00, 0x30, 0x05,
            0x06, 0x03, 0x2b, 0x65, 0x70, 0x04, 0x22, 0x04, 0x20
        ])
        pkcs8_der = pkcs8_prefix + seed_32_bytes
        pkcs8_b64 = base64.b64encode(pkcs8_der).decode('ascii')
        
        return f"-----BEGIN PRIVATE KEY-----\n{pkcs8_b64}\n-----END PRIVATE KEY-----"
    
    # Legacy format support
    COINBASE_API_KEY = "2636c881-b44e-4263-b05d-fb10a5ad1836"
    COINBASE_API_SECRET = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
    
    # Endpoint Configuration
    COINBASE_LIVE_URL = "https://api.coinbase.com"  # Advanced Trade LIVE ENDPOINT
    COINBASE_CDP_URL = "https://api.cdp.coinbase.com"  # CDP LIVE ENDPOINT
    COINBASE_ALGO = "ed25519"  # ED25519 signature algorithm
    
    # ========== RBOTZILLA ENHANCED SETTINGS ==========
    SWARM_MODE = True         # RBOTZILLA SWARM ACTIVATION
    
    # Capital & Risk Settings
    STARTING_CAPITAL = 3000
    RISK_PER_TRADE = 1.0   # 1% risk per trade
    MAX_TRADES_PER_DAY = 15
    MAX_CONCURRENT_TRADES = 3
    
    # Trading Pairs - RBOTZILLA SWARM TARGETS
    OANDA_PAIRS = [
        "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD",
        "USD/CHF", "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY",
        "AUD/JPY", "CHF/JPY"
    ]
    
    COINBASE_PAIRS = [
        "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "XRP-USD",
        "DOGE-USD", "AVAX-USD", "DOT-USD", "MATIC-USD", "LINK-USD",
        "ATOM-USD", "ALGO-USD"
    ]
    
    # FVG Strategy Settings
    MIN_GAP_PERCENT = 0.15
    MAX_FVG_AGE = 5
    MIN_RISK_REWARD = 2.5
    MIN_CONFLUENCE_SCORE = 7.0
    
    # Notification Settings
    ALERT_PHONE_NUMBER = "+16099006119"
    TELEGRAM_CHAT_ID = "7546584370"
    TELEGRAM_BOT_TOKEN = "8168818486:AAE3I8NBCNh5gSHXitmyAn4QQT3qrCL8yY0"
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1366149105168158761/DdhePkvCJltPvpUisbvSI_pIvlBrmQ-ZLzc-IRii0wGV3ZbhKDlkQphTqReLnniAh8W8"
    
    def validate_credentials(self):
        """RBOTZILLA Enhanced credential validation"""
        issues = []
        
        # Check Constitutional PIN
        if self.CONSTITUTIONAL_PIN != "841921":
            issues.append("Invalid Constitutional PIN")
            
        # Check OANDA
        if not self.OANDA_API_KEY or "your-" in self.OANDA_API_KEY:
            issues.append("OANDA API key not properly set")
            
        # Check Coinbase
        if not self.COINBASE_API_KEY_ID:
            issues.append("Coinbase API key ID missing")
            
        # Test PEM loading
        try:
            pem = self.COINBASE_PRIVATE_KEY_PEM
            if "BEGIN PRIVATE KEY" not in pem:
                issues.append("Coinbase PEM format invalid")
        except Exception as e:
            issues.append(f"Coinbase PEM loading failed: {e}")
            
        return issues
    
    def get_trading_summary(self):
        """Get RBOTZILLA swarm trading configuration summary"""
        return {
            "constitutional_pin": self.CONSTITUTIONAL_PIN,
            "swarm_mode": self.SWARM_MODE,
            "oanda_pairs": len(self.OANDA_PAIRS),
            "coinbase_pairs": len(self.COINBASE_PAIRS),
            "total_pairs": len(self.OANDA_PAIRS) + len(self.COINBASE_PAIRS),
            "risk_per_trade": f"{self.RISK_PER_TRADE}%",
            "min_rr": f"1:{self.MIN_RISK_REWARD}",
            "max_concurrent": self.MAX_CONCURRENT_TRADES,
        }
