#!/usr/bin/env python3
"""
🔥 CORRECTED COINBASE ED25519 AUTHENTICATION 
Based on analysis of your existing protocols
Constitutional PIN: 841921

JWT FORMAT CORRECTIONS:
✅ iss: 'cdp' (not the API key ID)
✅ sub: API key ID  
✅ uri: 'METHOD baseURL/path' format
✅ nonce: UUID4 in headers
✅ No aud field for Advanced Trade
"""

import os
import sys
import time
import json
import base64
import uuid
from typing import Dict, Any, Optional

sys.path.append('.')

def test_corrected_coinbase_auth():
    """Test with corrected JWT format based on existing protocols"""
    
    print("🔥 CORRECTED COINBASE ED25519 AUTHENTICATION TEST")
    print("=" * 60)
    print("Using JWT format from coinbase_advanced_api.py")
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        print("✅ Libraries and credentials loaded")
        
        # Load ED25519 private key
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
        
        print("✅ ED25519 private key loaded")
        
        # Test endpoint
        request_method = "GET"
        request_path = "/api/v3/brokerage/accounts"
        base_url = "https://api.coinbase.com"
        
        # Generate JWT with CORRECTED format (from coinbase_advanced_api.py)
        timestamp = int(time.time())
        
        payload = {
            'iss': 'cdp',  # Coinbase Developer Platform (not API key ID)
            'nbf': timestamp,
            'exp': timestamp + 120,  # 2 minutes expiration
            'sub': creds.COINBASE_API_KEY_ID,  # API key as subject
            'uri': f"{request_method.upper()} {base_url}{request_path}",  # Full URI format
        }
        
        # Generate PEM for signing
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # JWT headers with nonce
        jwt_headers = {
            'kid': creds.COINBASE_API_KEY_ID, 
            'nonce': str(uuid.uuid4())
        }
        
        jwt_token = jwt.encode(
            payload,
            pem_key,
            algorithm='EdDSA',
            headers=jwt_headers
        )
        
        print("✅ JWT token generated with corrected format")
        print(f"   iss: {payload['iss']}")
        print(f"   sub: {payload['sub']}")
        print(f"   uri: {payload['uri']}")
        print(f"   kid: {jwt_headers['kid']}")
        print(f"   Token: {jwt_token[:50]}...")
        
        # Make API request
        url = f"{base_url}{request_path}"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        print(f"\n📡 Making request to: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📡 Response: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS! Authentication working with corrected format")
            
            data = response.json()
            if 'accounts' in data:
                accounts = data['accounts']
                print(f"✅ Found {len(accounts)} accounts")
                
                for account in accounts:
                    currency = account.get('currency', 'Unknown')
                    balance = account.get('available_balance', {}).get('value', '0')
                    if float(balance) > 0:
                        print(f"   💰 {currency}: {balance}")
                        
            return True
            
        else:
            print(f"❌ Still getting error: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Try alternative JWT format
            return test_alternative_format(creds)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_alternative_format(creds):
    """Try alternative JWT format"""
    
    print("\n🔧 TRYING ALTERNATIVE JWT FORMAT")
    print("=" * 40)
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        # Load private key
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
        
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        timestamp = int(time.time())
        
        # Alternative format - minimal payload
        payload = {
            'iss': creds.COINBASE_API_KEY_ID,  # Try API key as issuer
            'exp': timestamp + 120,
            'iat': timestamp,
        }
        
        # Simple headers
        jwt_headers = {
            'alg': 'EdDSA',
            'kid': creds.COINBASE_API_KEY_ID,
            'typ': 'JWT'
        }
        
        jwt_token = jwt.encode(
            payload,
            pem_key,
            algorithm='EdDSA',
            headers=jwt_headers
        )
        
        print("✅ Alternative JWT format generated")
        print(f"   Format: Minimal payload")
        print(f"   iss: {payload['iss']}")
        
        # Test request
        url = "https://api.coinbase.com/api/v3/brokerage/accounts"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        print(f"📡 Alternative format response: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS with alternative format!")
            return True
        else:
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Alternative format failed: {e}")
        return False

def test_key_validity():
    """Test if the key itself is valid"""
    
    print("\n🔍 TESTING KEY VALIDITY")
    print("=" * 30)
    
    try:
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Test key decoding
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        print(f"✅ Seed decoded: {len(seed_bytes)} bytes")
        print(f"   Hex: {seed_bytes.hex()}")
        
        # Test ED25519 key creation
        from cryptography.hazmat.primitives.asymmetric import ed25519
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
        public_key = private_key.public_key()
        
        print(f"✅ ED25519 key pair created")
        
        # Test signature
        message = b"test message"
        signature = private_key.sign(message)
        
        # Verify signature
        try:
            public_key.verify(signature, message)
            print(f"✅ Signature verification successful")
            return True
        except Exception as e:
            print(f"❌ Signature verification failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Key validity test failed: {e}")
        return False

def main():
    """Main test with multiple formats"""
    
    print("🚀 COMPREHENSIVE COINBASE ED25519 TEST")
    print("Testing multiple JWT formats to find working solution")
    print("Constitutional PIN: 841921")
    print("=" * 60)
    
    # Test key validity first
    key_valid = test_key_validity()
    
    if not key_valid:
        print("❌ Key validation failed - check credential format")
        return False
    
    # Test corrected authentication
    auth_success = test_corrected_coinbase_auth()
    
    if auth_success:
        print("\n" + "="*60)
        print("🎉 COINBASE ED25519 AUTHENTICATION WORKING!")
        print("✅ JWT format identified and working")
        print("✅ API access confirmed")  
        print("🔐 Constitutional PIN: 841921")
        print("🚀 Ready for trading system integration")
    else:
        print("\n❌ Authentication still failing")
        print("💡 Next steps:")
        print("1. Check API key status in Coinbase Developer Console")
        print("2. Verify API key has 'trade' permissions")
        print("3. Try regenerating API key if needed")
        print("4. Check if account requires additional verification")

if __name__ == "__main__":
    main()
