#!/usr/bin/env python3
"""
🔐 COINBASE ECDSA CREDENTIALS TEMPLATE
Constitutional PIN: 841921

CRITICAL SETUP FOR LIVE MONEY TRADING:
✅ ECDSA authentication (required by Coinbase SDK)
✅ Proper PEM key format for JWT generation
✅ Live endpoints only - NO SANDBOX
✅ Real money trading credentials
"""

class CoinbaseECDSACredentials:
    """
    🔥 COINBASE ADVANCED TRADING ECDSA CREDENTIALS
    Template for AI agent implementation
    """
    
    def __init__(self):
        print("🔐 COINBASE ECDSA CREDENTIALS LOADED")
        print("🔴 LIVE MONEY TRADING MODE")
        print("🔐 Constitutional PIN: 841921")
    
    # ========== COINBASE ECDSA LIVE CREDENTIALS ==========
    
    # STEP 1: Replace with your actual API key ID
    # This comes from the "name" field in your downloaded JSON
    COINBASE_API_KEY = "your-api-key-id-here"  # Example: "2636c881-b44e-4263-b05d-fb10a5ad1836"
    
    # STEP 2: Replace with your ECDSA private key in PEM format
    # This comes from the "privateKey" field in your downloaded JSON
    # MUST be ECDSA format (NOT Ed25519)
    COINBASE_PRIVATE_KEY_ECDSA = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIYour-ECDSA-private-key-content-goes-here-replace-this-with-actual-key
-----END EC PRIVATE KEY-----"""
    
    # STEP 3: Alternative base64 format (if needed)
    # Some implementations may need the raw base64 key
    COINBASE_PRIVATE_KEY_BASE64 = "your-base64-ecdsa-key-here"
    
    # ========== COINBASE LIVE ENDPOINTS ==========
    
    # Live trading endpoints (NO SANDBOX)
    COINBASE_LIVE_URL = "https://api.coinbase.com"  # Advanced Trade LIVE
    COINBASE_WS_URL = "wss://advanced-trade-ws.coinbase.com"  # WebSocket LIVE
    
    # Authentication method
    COINBASE_AUTH_METHOD = "ECDSA"  # Required by SDK
    COINBASE_SIGNATURE_ALGO = "ES256"  # ECDSA with SHA-256
    
    # ========== TRADING CONFIGURATION ==========
    
    # Risk management settings
    MAX_ORDER_SIZE_USD = 1000.0      # Maximum $1000 per order
    MIN_ORDER_SIZE_USD = 10.0        # Minimum $10 per order
    MAX_DAILY_TRADES = 50            # Daily trade limit
    MAX_CONCURRENT_ORDERS = 10       # Maximum open orders
    
    # Supported trading pairs for live trading
    COINBASE_LIVE_PAIRS = [
        "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "XRP-USD",
        "DOGE-USD", "AVAX-USD", "DOT-USD", "MATIC-USD", "LINK-USD",
        "ATOM-USD", "ALGO-USD", "LTC-USD", "BCH-USD", "NEAR-USD",
        "UNI-USD", "AAVE-USD", "COMP-USD", "MKR-USD", "SNX-USD"
    ]
    
    # ========== SECURITY SETTINGS ==========
    
    CONSTITUTIONAL_PIN = "841921"    # Security verification
    REQUIRE_ECDSA = True            # ECDSA authentication required
    
    # ========== VALIDATION METHODS ==========
    
    def validate_ecdsa_credentials(self):
        """Validate ECDSA credentials format"""
        print("\n🔍 VALIDATING ECDSA CREDENTIALS...")
        
        issues = []
        
        # Check API key format
        if self.COINBASE_API_KEY == "your-api-key-id-here":
            issues.append("❌ API Key not configured (still placeholder)")
        elif not self.COINBASE_API_KEY or len(self.COINBASE_API_KEY) < 10:
            issues.append("❌ API Key appears invalid")
        else:
            print("✅ API Key format OK")
        
        # Check ECDSA private key format
        if "your-ECDSA-private-key-content" in self.COINBASE_PRIVATE_KEY_ECDSA:
            issues.append("❌ ECDSA Private Key not configured (still placeholder)")
        elif not self.COINBASE_PRIVATE_KEY_ECDSA.startswith("-----BEGIN EC PRIVATE KEY-----"):
            issues.append("❌ ECDSA Private Key wrong format (must be PEM)")
        elif not self.COINBASE_PRIVATE_KEY_ECDSA.endswith("-----END EC PRIVATE KEY-----"):
            issues.append("❌ ECDSA Private Key incomplete (missing end marker)")
        else:
            print("✅ ECDSA Private Key format OK")
        
        # Check for Ed25519 keys (not supported)
        if "ED25519" in self.COINBASE_PRIVATE_KEY_ECDSA.upper():
            issues.append("❌ Ed25519 key detected - SDK requires ECDSA")
        
        # Report results
        if issues:
            print("\n🚨 CREDENTIAL VALIDATION FAILED:")
            for issue in issues:
                print(f"   {issue}")
            return False
        else:
            print("\n✅ CREDENTIAL VALIDATION PASSED")
            print("🚀 Ready for live trading setup")
            return True
    
    def get_setup_instructions(self):
        """Get detailed setup instructions"""
        return """
🔧 COINBASE ECDSA SETUP INSTRUCTIONS
====================================

STEP 1: Get API Credentials
---------------------------
1. Go to: https://portal.cdp.coinbase.com/access/api
2. Click "Create API Key"
3. IMPORTANT: Click "Advanced Settings"
4. Select "ECDSA" algorithm (NOT Ed25519)
5. Select "trade" permissions for live trading
6. Download the JSON credentials file

STEP 2: Extract Credentials
---------------------------
From your downloaded JSON file:
{
  "name": "organizations/your-org/apiKeys/12345678-1234-1234-1234-123456789abc",
  "privateKey": "-----BEGIN EC PRIVATE KEY-----\\nMHcCAQEEI...\\n-----END EC PRIVATE KEY-----\\n"
}

Copy the values:
- API Key = the UUID part from "name" field
- Private Key = the entire "privateKey" field (including BEGIN/END lines)

STEP 3: Update Credentials
--------------------------
Replace the placeholders in this file:
- COINBASE_API_KEY = "12345678-1234-1234-1234-123456789abc"
- COINBASE_PRIVATE_KEY_ECDSA = "-----BEGIN EC PRIVATE KEY-----\\n...\\n-----END EC PRIVATE KEY-----"

STEP 4: Test Connection
-----------------------
```python
from coinbase_ecdsa_credentials import CoinbaseECDSACredentials

creds = CoinbaseECDSACredentials()
if creds.validate_ecdsa_credentials():
    print("✅ Ready for live trading!")
else:
    print("❌ Fix credential issues first")
```

CRITICAL WARNINGS
-----------------
🔴 LIVE MONEY AT RISK - NO SANDBOX MODE
🔴 Start with small test amounts
🔴 Double-check all orders before placement
🔴 Keep your private key secure and never share it
🔴 ECDSA is required - Ed25519 will NOT work with the SDK

Constitutional PIN: 841921
"""
    
    def display_config(self):
        """Display current configuration (safely)"""
        print("\n📋 COINBASE ECDSA CONFIGURATION")
        print("=" * 50)
        print(f"🔐 Constitutional PIN: {self.CONSTITUTIONAL_PIN}")
        print(f"🌐 Live URL: {self.COINBASE_LIVE_URL}")
        print(f"🔒 Auth Method: {self.COINBASE_AUTH_METHOD}")
        print(f"📊 Max Order Size: ${self.MAX_ORDER_SIZE_USD}")
        print(f"📊 Max Daily Trades: {self.MAX_DAILY_TRADES}")
        print(f"💰 Supported Pairs: {len(self.COINBASE_LIVE_PAIRS)} pairs")
        
        # Show API key status (safely)
        if self.COINBASE_API_KEY == "your-api-key-id-here":
            print("🔑 API Key: ❌ NOT CONFIGURED")
        else:
            key_preview = self.COINBASE_API_KEY[:8] + "..." + self.COINBASE_API_KEY[-4:]
            print(f"🔑 API Key: ✅ {key_preview}")
        
        # Show private key status (safely)
        if "your-ECDSA-private-key-content" in self.COINBASE_PRIVATE_KEY_ECDSA:
            print("🔐 Private Key: ❌ NOT CONFIGURED")
        else:
            print("🔐 Private Key: ✅ CONFIGURED (ECDSA format)")


def test_ecdsa_key_format():
    """Test ECDSA key format validation"""
    print("🧪 TESTING ECDSA KEY FORMAT VALIDATION")
    print("=" * 50)
    
    # Test valid ECDSA key format
    valid_ecdsa = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIExample123456789012345678901234567890123456789012
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
-----END EC PRIVATE KEY-----"""
    
    # Test invalid formats
    invalid_formats = [
        "not-a-key-at-all",
        "-----BEGIN PRIVATE KEY-----\nwrong-format\n-----END PRIVATE KEY-----",
        "-----BEGIN ED25519 PRIVATE KEY-----\ned25519-key\n-----END ED25519 PRIVATE KEY-----"
    ]
    
    print("✅ Valid ECDSA format example:")
    print(f"   {valid_ecdsa[:50]}...")
    
    print("\n❌ Invalid formats:")
    for i, invalid in enumerate(invalid_formats, 1):
        print(f"   {i}. {invalid[:30]}...")
    
    print("\n🔍 Key validation checks:")
    print("   ✅ Must start with '-----BEGIN EC PRIVATE KEY-----'")
    print("   ✅ Must end with '-----END EC PRIVATE KEY-----'")
    print("   ❌ Ed25519 keys are NOT supported by SDK")
    print("   ❌ Plain text keys are NOT valid")


if __name__ == "__main__":
    print("🔥 COINBASE ECDSA CREDENTIALS TEMPLATE")
    print("=" * 60)
    print("🔴 WARNING: FOR LIVE MONEY TRADING ONLY")
    print("🔐 Constitutional PIN: 841921")
    print("=" * 60)
    
    # Initialize credentials
    creds = CoinbaseECDSACredentials()
    
    # Display configuration
    creds.display_config()
    
    # Show setup instructions
    print(creds.get_setup_instructions())
    
    # Test key format validation
    test_ecdsa_key_format()
    
    # Validate current credentials
    print("\n" + "=" * 60)
    print("🔍 VALIDATING CURRENT CREDENTIALS")
    creds.validate_ecdsa_credentials()
    
    print("\n" + "=" * 60)
    print("🚀 NEXT STEPS:")
    print("1. Get your ECDSA credentials from Coinbase")
    print("2. Update the placeholders in this file")
    print("3. Run validation again")
    print("4. Initialize live trading system")
    print("=" * 60)
