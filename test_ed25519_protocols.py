#!/usr/bin/env python3
"""
🎯 COINBASE ED25519 PROTOCOL COMPREHENSIVE TEST
Constitutional PIN: 841921
Testing all Ed25519 authentication variants from your attached protocols

PROTOCOLS TO TEST:
1. Advanced Trading API (EdDSA + cdp issuer)
2. CDP Platform API (coinbase-cloud issuer)
3. Direct Advanced Trading (API key issuer)
4. Minimal EdDSA format
"""

import os
import sys
import time
import json
import base64
import uuid
from typing import Dict, Any, Optional

sys.path.append('.')

def test_advanced_trading_edDSA():
    """Test Advanced Trading API with EdDSA from coinbase_jwt_auth.py protocol"""
    
    print("🔧 TESTING ADVANCED TRADING EdDSA")
    print("=" * 40)
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Load Ed25519 private key from PEM (your working format)
        private_key = serialization.load_pem_private_key(
            creds.COINBASE_PRIVATE_KEY_PEM.encode(),
            password=None
        )
        
        print("✅ Ed25519 private key loaded from PEM")
        
        # Advanced Trading format (from your coinbase_jwt_auth.py)
        current_time = int(time.time())
        
        payload = {
            "iss": creds.COINBASE_API_KEY_ID,  # API key as issuer
            "exp": current_time + 180,  # 3 minutes
            "iat": current_time
        }
        
        headers = {
            "alg": "EdDSA",  # Ed25519 algorithm
            "kid": creds.COINBASE_API_KEY_ID,
            "typ": "JWT"
        }
        
        jwt_token = jwt.encode(payload, private_key, algorithm="EdDSA", headers=headers)
        
        print(f"✅ Advanced Trading EdDSA token generated")
        
        # Test request
        url = "https://api.coinbase.com/api/v3/brokerage/accounts"
        request_headers = {
            "Authorization": f"Bearer {jwt_token}",
            "CB-ACCESS-KEY": creds.COINBASE_API_KEY_ID,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=request_headers, timeout=30)
        print(f"📡 Advanced Trading EdDSA response: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS with Advanced Trading EdDSA!")
            return True, response.json()
        else:
            print(f"Response: {response.text[:200]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ Advanced Trading EdDSA failed: {e}")
        return False, None

def test_cdp_platform_edDSA():
    """Test CDP Platform API with coinbase-cloud issuer from cdp_jwt_auth.py"""
    
    print("\n🔧 TESTING CDP PLATFORM EdDSA")
    print("=" * 40)
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Load Ed25519 private key from seed (32 bytes)
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
        
        print("✅ Ed25519 private key loaded from seed")
        
        # CDP Platform format (from your cdp_jwt_auth.py)
        current_time = int(time.time())
        
        payload = {
            'iss': 'coinbase-cloud',  # CDP issuer
            'nbf': current_time,
            'exp': current_time + 120,  # 2 minutes
            'sub': creds.COINBASE_API_KEY_ID,
            'aud': ['retail_rest_api_proxy']
        }
        
        jwt_token = jwt.encode(payload, private_key, algorithm='EdDSA')
        
        print(f"✅ CDP Platform EdDSA token generated")
        
        # Test CDP endpoint
        url = "https://api.cdp.coinbase.com/platform/v1/networks"
        request_headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=request_headers, timeout=30)
        print(f"📡 CDP Platform EdDSA response: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS with CDP Platform EdDSA!")
            return True, response.json()
        else:
            print(f"Response: {response.text[:200]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ CDP Platform EdDSA failed: {e}")
        return False, None

def test_advanced_trade_cdp_format():
    """Test Advanced Trade API with 'cdp' issuer format"""
    
    print("\n🔧 TESTING ADVANCED TRADE CDP FORMAT")
    print("=" * 40)
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Load Ed25519 private key from PEM
        private_key = serialization.load_pem_private_key(
            creds.COINBASE_PRIVATE_KEY_PEM.encode(),
            password=None
        )
        
        print("✅ Ed25519 private key loaded from PEM")
        
        # Advanced Trade with CDP issuer format
        request_method = "GET"
        request_path = "/api/v3/brokerage/accounts"
        request_host = "api.coinbase.com"
        
        current_time = int(time.time())
        
        payload = {
            "iss": "cdp",  # CDP issuer
            "nbf": current_time,
            "exp": current_time + 120,
            "sub": creds.COINBASE_API_KEY_ID,
            "uri": f"{request_method} {request_host}{request_path}",
            "aud": ["cdp_service"]
        }
        
        headers = {
            "kid": creds.COINBASE_API_KEY_ID,
            "nonce": str(uuid.uuid4()),
            "typ": "JWT",
            "alg": "EdDSA"
        }
        
        jwt_token = jwt.encode(payload, private_key, algorithm="EdDSA", headers=headers)
        
        print(f"✅ Advanced Trade CDP format token generated")
        
        # Test request
        url = f"https://{request_host}{request_path}"
        request_headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=request_headers, timeout=30)
        print(f"📡 Advanced Trade CDP format response: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS with Advanced Trade CDP format!")
            return True, response.json()
        else:
            print(f"Response: {response.text[:200]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ Advanced Trade CDP format failed: {e}")
        return False, None

def test_deterministic_seed_method():
    """Test using SHA-256 derived seed from test_advanced_jwt.py"""
    
    print("\n🔧 TESTING DETERMINISTIC SEED METHOD")
    print("=" * 40)
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        import hashlib
        import requests
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Generate deterministic seed from private key string (Method 3 from test_advanced_jwt.py)
        seed = hashlib.sha256(creds.COINBASE_PRIVATE_KEY.encode()).digest()
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
        
        print("✅ Ed25519 private key from SHA-256 deterministic seed")
        
        # Advanced Trading format
        current_time = int(time.time())
        
        payload = {
            'iss': 'coinbase-cloud',
            'nbf': current_time,
            'exp': current_time + 120,  # 2 minutes
            'sub': creds.COINBASE_API_KEY_ID,
            'aud': ['retail_rest_api_proxy']
        }
        
        jwt_token = jwt.encode(payload, private_key, algorithm='EdDSA')
        
        print(f"✅ Deterministic seed EdDSA token generated")
        
        # Test request
        url = "https://api.coinbase.com/api/v3/brokerage/accounts"
        request_headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=request_headers, timeout=30)
        print(f"📡 Deterministic seed response: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS with Deterministic seed method!")
            return True, response.json()
        else:
            print(f"Response: {response.text[:200]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ Deterministic seed method failed: {e}")
        return False, None

def validate_ed25519_key():
    """Validate that Ed25519 key is working properly"""
    
    print("\n🔍 VALIDATING Ed25519 KEY")
    print("=" * 30)
    
    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Test PEM format
        try:
            private_key = serialization.load_pem_private_key(
                creds.COINBASE_PRIVATE_KEY_PEM.encode(),
                password=None
            )
            
            # Test signing
            test_data = b"test message"
            signature = private_key.sign(test_data)
            
            # Verify with public key
            public_key = private_key.public_key()
            public_key.verify(signature, test_data)
            
            print("✅ Ed25519 PEM key validation successful")
            print(f"   Key type: {type(private_key)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ed25519 PEM validation failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Ed25519 validation error: {e}")
        return False

def display_credential_info():
    """Display credential information for debugging"""
    
    print("\n📋 CREDENTIAL INFORMATION")
    print("=" * 30)
    
    try:
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        print(f"API Key ID: {creds.COINBASE_API_KEY_ID}")
        print(f"API Key Length: {len(creds.COINBASE_API_KEY_ID)} characters")
        
        print(f"\nPrivate Key (64-byte): {len(creds.COINBASE_PRIVATE_KEY)} chars")
        print(f"Private Key Seed (32-byte): {len(creds.COINBASE_PRIVATE_KEY_SEED)} chars")
        print(f"Private Key Hex: {len(creds.COINBASE_PRIVATE_KEY_HEX)} chars")
        
        print(f"\nEndpoints:")
        print(f"Advanced Trade: {creds.COINBASE_LIVE_URL}")
        print(f"CDP Platform: {creds.COINBASE_CDP_URL}")
        print(f"Algorithm: {creds.COINBASE_ALGO}")
        
    except Exception as e:
        print(f"❌ Credential info error: {e}")

def main():
    """Test all Ed25519 authentication protocols"""
    
    print("🎯 COINBASE ED25519 PROTOCOL COMPREHENSIVE TEST")
    print("Constitutional PIN: 841921")
    print("Testing Ed25519 authentication from your attached protocols")
    print("=" * 60)
    
    # Display credential info
    display_credential_info()
    
    # Validate Ed25519 key first
    if not validate_ed25519_key():
        print("❌ Ed25519 key validation failed - cannot proceed")
        return
    
    # Test all protocols
    protocols = [
        ("Advanced Trading EdDSA", test_advanced_trading_edDSA),
        ("CDP Platform EdDSA", test_cdp_platform_edDSA),
        ("Advanced Trade CDP Format", test_advanced_trade_cdp_format),
        ("Deterministic Seed Method", test_deterministic_seed_method)
    ]
    
    success_count = 0
    working_protocol = None
    
    for protocol_name, test_func in protocols:
        try:
            success, data = test_func()
            if success:
                print(f"🎉 {protocol_name}: SUCCESS!")
                working_protocol = protocol_name
                success_count += 1
                
                if data and 'accounts' in data:
                    accounts = data['accounts']
                    print(f"   Found {len(accounts)} accounts")
                elif data:
                    print(f"   Response data keys: {list(data.keys())}")
                break
            else:
                print(f"❌ {protocol_name}: Failed")
                
        except Exception as e:
            print(f"❌ {protocol_name}: Exception - {e}")
    
    print(f"\n📊 RESULTS SUMMARY")
    print("=" * 30)
    
    if success_count > 0:
        print(f"✅ SUCCESS! {working_protocol} is working")
        print("🚀 Ed25519 authentication ready for trading system integration")
        
        print(f"\n🔧 INTEGRATION NOTES:")
        print("• Use EdDSA algorithm (not ES256)")
        print("• Ed25519 key validation successful")
        print("• JWT token generation working")
        print("• Live API endpoints responding")
        
    else:
        print("❌ ALL Ed25519 PROTOCOLS FAILED")
        print("\n💡 POSSIBLE ISSUES:")
        print("• API key may be expired or deactivated")
        print("• API key may not have required permissions")
        print("• Account may need additional verification")
        print("• Coinbase may have changed authentication requirements")
        
        print(f"\n🔄 NEXT STEPS:")
        print("1. Check Coinbase Developer Portal for API key status")
        print("2. Verify API key permissions (view, trade, etc.)")
        print("3. Ensure account is fully verified")
        print("4. Consider regenerating API keys if needed")

if __name__ == "__main__":
    main()
