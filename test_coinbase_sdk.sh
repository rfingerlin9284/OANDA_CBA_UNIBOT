#!/bin/bash
#!/usr/bin/env python3
"""
🔧 COINBASE ADVANCED TRADE SDK AUTHENTICATION TEST
Test official SDK with ED25519 credentials
"""

import sys
sys.path.append('.')

try:
    from coinbase.rest import RESTClient
    print("✅ Coinbase SDK imported successfully")
except ImportError as e:
    print(f"❌ Coinbase SDK import failed: {e}")
    print("Install with: pip install coinbase-advanced-py")
    sys.exit(1)

from credentials import WolfpackCredentials

    """Test Coinbase Advanced Trade SDK authentication"""
    print("🔧 TESTING COINBASE SDK AUTHENTICATION...")
    print("=" * 50)
    
    try:
        # Load credentials
        creds = WolfpackCredentials()
        
        print(f"API Key: {creds.COINBASE_API_KEY}")
        print(f"API Secret (first 20 chars): {creds.COINBASE_API_SECRET[:20]}...")
        
        # Initialize REST client
        client = RESTClient(
            api_key=creds.COINBASE_API_KEY,
            api_secret=creds.COINBASE_API_SECRET
        )
        
        print("✅ RESTClient initialized")
        
        # Test 1: Get accounts
        print("\n📊 Testing get_accounts()...")
        accounts_response = client.get_accounts()
        
        if accounts_response and hasattr(accounts_response, 'accounts'):
            accounts = accounts_response.accounts
            print(f"✅ Accounts retrieved: {len(accounts)} found")
            
            # Show account details
            for i, account in enumerate(accounts[:3]):  # Show first 3
                currency = getattr(account, 'currency', 'Unknown')
                available = getattr(account, 'available_balance', None)
                balance_value = getattr(available, 'value', '0') if available else '0'
                print(f"   Account {i+1}: {currency} = {balance_value}")
        else:
            print("⚠️ Accounts response format unexpected")
            print(f"Response: {accounts_response}")
        
        # Test 2: Get products
        print("\n📊 Testing get_products()...")
        products_response = client.get_products()
        
        if products_response and hasattr(products_response, 'products'):
            products = products_response.products
            crypto_products = [p for p in products if hasattr(p, 'product_id') and 'USD' in p.product_id]
            
            print(f"✅ Products retrieved: {len(products)} total, {len(crypto_products)} crypto pairs")
            
            # Show some crypto products
            for i, product in enumerate(crypto_products[:5]):
                product_id = getattr(product, 'product_id', 'Unknown')
                status = getattr(product, 'status', 'Unknown')
                print(f"   Product {i+1}: {product_id} ({status})")
        else:
            print("⚠️ Products response format unexpected")
            print(f"Response: {products_response}")
        
        print("\n🚀 COINBASE SDK AUTHENTICATION SUCCESS!")
        print("✅ ED25519 JWT working with official SDK")
        print("✅ Ready for live trading integration")
        return True
        
    except Exception as e:
        print(f"\n❌ COINBASE SDK TEST FAILED: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    if success:
        print("\n🎯 SDK INTEGRATION READY")
        exit(0)
    else:
        print("\n⚠️ SDK INTEGRATION FAILED")
        exit(1)
EOF

