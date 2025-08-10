# ✅ PATCHED: Coinbase API Credential Access
# 🧠 Injected: Aug 5, 2025
# Constitutional PIN: 841921

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from credentials import WolfpackCredentials

class CoinbaseAuth:
    """
    🔐 PATCHED COINBASE AUTHENTICATION CLASS
    Constitutional PIN: 841921
    """
    
    def __init__(self):
        self.creds = WolfpackCredentials()
        print("✅ Coinbase Auth Patched - Credentials Loaded Successfully")

    def get_headers(self):
        """Get authentication headers for Coinbase API"""
        return {
            "CB-ACCESS-KEY": self.creds.COINBASE_API_KEY_ID,
            "CB-ACCESS-SIGN": self.creds.COINBASE_PRIVATE_KEY,  # Will be properly signed
            "CB-ACCESS-TIMESTAMP": str(int(time.time())),
            "CB-ACCESS-PASSPHRASE": self.creds.COINBASE_API_SECRET,
            "Content-Type": "application/json"
        }

    def get_auth_tuple(self):
        """Get authentication tuple for API calls"""
        return (self.creds.COINBASE_API_KEY_ID, self.creds.COINBASE_PRIVATE_KEY)
        
    def get_credentials(self):
        """Direct credential access - PATCHED"""
        return {
            'api_key_id': self.creds.COINBASE_API_KEY_ID,
            'private_key': self.creds.COINBASE_PRIVATE_KEY,
            'private_key_pem': self.creds.COINBASE_PRIVATE_KEY_PEM,
            'algorithm': self.creds.COINBASE_ALGO,
            'base_url': self.creds.COINBASE_LIVE_URL
        }
