#!/usr/bin/env python3
"""
🔐 ED25519 AUTHENTICATION TEST
Test OANDA and Coinbase Advanced Trade API authentication
"""

import sys
import os
sys.path.append('.')

def test_oanda_auth():
    """Test OANDA API authentication"""
    print("📊 Testing OANDA Live API Authentication...")
    try:
        import oandapyV20
        from oandapyV20.endpoints.accounts import AccountSummary
        from credentials import WolfpackCredentials
        
        creds = WolfpackCredentials()
        api = oandapyV20.API(
            access_token=creds.OANDA_API_KEY,
            environment='live'
        )
        
        # Test account access
        r = AccountSummary(accountID=creds.OANDA_ACCOUNT_ID)
        response = api.request(r)
        
        balance = float(response['account']['balance'])
        unrealized_pl = float(response['account']['unrealizedPL'])
        open_trades = int(response['account']['openTradeCount'])
        
        print(f"✅ OANDA API Connected Successfully!")
        print(f"   Account ID: {creds.OANDA_ACCOUNT_ID}")
        print(f"   Balance: ${balance:,.2f}")
        print(f"   Unrealized P&L: ${unrealized_pl:,.2f}")
        print(f"   Open Trades: {open_trades}")
        return True
        
    except Exception as e:
        print(f"❌ OANDA API Error: {e}")
        return False

def test_coinbase_ed25519_auth():
    """Test Coinbase Advanced Trade ED25519 authentication"""
    print("\n₿ Testing Coinbase Advanced Trade ED25519 Authentication...")
    try:
        from coinbase_advanced_api import CoinbaseAdvancedTradeAPI
        from credentials import WolfpackCredentials
        
        creds = WolfpackCredentials()
        
        # Initialize Coinbase client with ED25519
        cb_api = CoinbaseAdvancedTradeAPI(
            api_key=creds.COINBASE_API_KEY,
            private_key_b64=creds.COINBASE_PRIVATE_KEY_B64
        )
        
        # Test API connection
        products = cb_api.list_products()
        accounts = cb_api.get_accounts()
        
        print(f"✅ Coinbase Advanced Trade API Connected Successfully!")
        print(f"   API Key: {creds.COINBASE_API_KEY}")
        print(f"   Algorithm: ED25519 ✅")
        print(f"   Available Products: {len(products)}")
        print(f"   Active Accounts: {len(accounts)}")
        
        # Show balances for accounts with funds
        usd_balance = 0
        for account in accounts:
            if account.get('currency') == 'USD' and float(account.get('available_balance', {}).get('value', 0)) > 0:
                usd_balance = float(account.get('available_balance', {}).get('value', 0))
                break
                
        if usd_balance > 0:
            print(f"   USD Balance: ${usd_balance:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Coinbase ED25519 API Error: {e}")
        return False

def test_environment_variables():
    """Test environment variable configuration"""
    print("\n🔧 Testing Environment Variables...")
    try:
        # Load .env file
        env_vars = {}
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
        
        # Check critical variables
        required_vars = [
            'CONSTITUTIONAL_PIN',
            'OANDA_API_KEY', 
            'OANDA_ACCOUNT_ID',
            'COINBASE_API_KEY_ID',
            'COINBASE_API_KEY_SECRET_PEM',
            'COINBASE_API_ALGO'
        ]
        
        missing = []
        for var in required_vars:
            if var not in env_vars:
                missing.append(var)
        
        if missing:
            print(f"❌ Missing environment variables: {missing}")
            return False
        else:
            print("✅ All required environment variables present")
            
        # Verify ED25519 format
        if env_vars.get('COINBASE_API_ALGO') == 'ed25519':
            print("✅ ED25519 algorithm specified")
        else:
            print("❌ ED25519 algorithm not specified")
            
        # Verify PEM format
        pem_key = env_vars.get('COINBASE_API_KEY_SECRET_PEM', '')
        if '-----BEGIN PRIVATE KEY-----' in pem_key:
            print("✅ ED25519 PEM private key format correct")
        else:
            print("❌ ED25519 PEM private key format incorrect")
            
        return True
        
    except Exception as e:
        print(f"❌ Environment test error: {e}")
        return False

def main():
    """Run all authentication tests"""
    print("🔐 WOLFPACK-LITE API AUTHENTICATION TEST")
    print("=" * 50)
    
    results = []
    
    # Test environment variables
    results.append(("Environment Variables", test_environment_variables()))
    
    # Test OANDA
    results.append(("OANDA API", test_oanda_auth()))
    
    # Test Coinbase ED25519
    results.append(("Coinbase ED25519", test_coinbase_ed25519_auth()))
    
    # Summary
    print("\n🎯 AUTHENTICATION TEST SUMMARY")
    print("=" * 40)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 40)
    if all_passed:
        print("🚀 ALL TESTS PASSED - READY FOR LIVE TRADING!")
        print("Constitutional PIN: 841921")
    else:
        print("⚠️  SOME TESTS FAILED - CHECK CREDENTIALS")
    
    return all_passed

if __name__ == "__main__":
    main()
