#!/usr/bin/env python3
"""
🔥 LIVE COINBASE ED25519 AUTHENTICATION TEST
Uses virtual environment with proper dependencies
Tests your JSON credentials with real API calls

Constitutional PIN: 841921
"""

import os
import sys
import time
import json
import base64
import uuid
from typing import Dict, Any, Optional

# Add current directory to path
sys.path.append('.')

def test_coinbase_authentication():
    """Test live Coinbase ED25519 authentication"""
    
    print("🔐 LIVE COINBASE ED25519 AUTHENTICATION TEST")
    print("=" * 60)
    
    try:
        # Import required libraries
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        print("✅ All required libraries imported successfully")
        
        # Load credentials
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        print(f"✅ Credentials loaded")
        print(f"   API Key ID: {creds.COINBASE_API_KEY_ID}")
        print(f"   Private Key Seed: {creds.COINBASE_PRIVATE_KEY_SEED}")
        
        # Load ED25519 private key from seed
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
        
        print(f"✅ ED25519 private key loaded from seed")
        
        # Generate PEM format for JWT
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        print(f"✅ PEM format generated")
        
        # Generate JWT token
        current_time = int(time.time())
        
        payload = {
            "iss": creds.COINBASE_API_KEY_ID,
            "sub": creds.COINBASE_API_KEY_ID,
            "aud": ["coinbase-advanced-trade"],
            "iat": current_time,
            "exp": current_time + 120,
            "nbf": current_time,
            "jti": str(uuid.uuid4())
        }
        
        headers_jwt = {
            "alg": "EdDSA",
            "typ": "JWT",
            "kid": creds.COINBASE_API_KEY_ID
        }
        
        jwt_token = jwt.encode(payload, pem_key, algorithm="EdDSA", headers=headers_jwt)
        
        print(f"✅ JWT token generated successfully")
        print(f"   Token length: {len(jwt_token)} characters")
        print(f"   Token preview: {jwt_token[:50]}...")
        
        # Make API request
        url = "https://api.coinbase.com/api/v3/brokerage/accounts"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        print(f"\n📡 Making API request to: {url}")
        
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("🎉 AUTHENTICATION SUCCESSFUL!")
            print(f"✅ Response received: {len(data)} items")
            
            if 'accounts' in data:
                accounts = data['accounts']
                print(f"✅ Found {len(accounts)} accounts")
                
                # Show account balances
                for account in accounts:
                    currency = account.get('currency', 'Unknown')
                    balance = account.get('available_balance', {}).get('value', '0')
                    if float(balance) > 0:
                        print(f"   💰 {currency}: {balance}")
                
                return True
            else:
                print("⚠️  Accounts data not in expected format")
                print(f"Response keys: {list(data.keys())}")
                return False
        
        elif response.status_code == 401:
            print("❌ AUTHENTICATION FAILED - 401 Unauthorized")
            print("💡 Possible issues:")
            print("   - API key may be expired or invalid")
            print("   - JWT signature may be incorrect")
            print("   - Clock synchronization issue")
            print(f"Response: {response.text}")
            return False
            
        elif response.status_code == 403:
            print("❌ FORBIDDEN - 403")
            print("💡 API key may not have required permissions")
            print(f"Response: {response.text}")
            return False
            
        else:
            print(f"❌ API ERROR - {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
    except ImportError as e:
        print(f"❌ Missing required library: {e}")
        print("💡 Make sure virtual environment is activated")
        return False
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def test_products_endpoint():
    """Test the products endpoint"""
    
    print("\n📊 TESTING PRODUCTS ENDPOINT")
    print("=" * 40)
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Load private key
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
        
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Generate JWT
        current_time = int(time.time())
        payload = {
            "iss": creds.COINBASE_API_KEY_ID,
            "sub": creds.COINBASE_API_KEY_ID,
            "aud": ["coinbase-advanced-trade"],
            "iat": current_time,
            "exp": current_time + 120,
            "nbf": current_time,
            "jti": str(uuid.uuid4())
        }
        
        headers_jwt = {
            "alg": "EdDSA",
            "typ": "JWT", 
            "kid": creds.COINBASE_API_KEY_ID
        }
        
        jwt_token = jwt.encode(payload, pem_key, algorithm="EdDSA", headers=headers_jwt)
        
        # Make products request
        url = "https://api.coinbase.com/api/v3/brokerage/products"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'products' in data:
                products = data['products']
                print(f"✅ Found {len(products)} trading products")
                
                # Show popular crypto pairs
                popular_pairs = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD']
                for product in products:
                    if product.get('product_id') in popular_pairs:
                        status = product.get('status', 'unknown')
                        print(f"   📈 {product.get('product_id')}: {status}")
                
                return True
        else:
            print(f"❌ Products request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Products test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 COINBASE ED25519 AUTHENTICATION - LIVE TEST")
    print("Using virtual environment with proper dependencies")
    print("Constitutional PIN: 841921")
    print("=" * 60)
    
    # Test authentication
    auth_success = test_coinbase_authentication()
    
    if auth_success:
        # Test products
        products_success = test_products_endpoint()
        
        if products_success:
            print("\n" + "="*60)
            print("🎉 ALL TESTS SUCCESSFUL!")
            print("✅ Coinbase ED25519 authentication is working")
            print("✅ API endpoints are accessible")
            print("✅ Ready for live trading integration")
            print("🔐 Constitutional PIN: 841921")
            
            print("\n🔧 INTEGRATION READY:")
            print("- Use WorkingCoinbaseED25519Auth class")
            print("- JSON credentials are properly formatted")
            print("- ED25519 JWT authentication confirmed")
            print("- Live Coinbase Advanced Trade API access verified")
            
        else:
            print("\n⚠️  Authentication works but products endpoint failed")
    else:
        print("\n❌ Authentication failed - check API key status")
        print("💡 Possible solutions:")
        print("1. Verify API key is still active in Coinbase console")
        print("2. Check API key permissions include 'trade' access")
        print("3. Ensure system clock is synchronized")

if __name__ == "__main__":
    main()
