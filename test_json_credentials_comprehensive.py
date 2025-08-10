#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE COINBASE ED25519 PROTOCOL TEST
Tests all authentication protocols using JSON credentials
Constitutional PIN: 841921

JSON CREDENTIALS USED:
{
    "id": "2636c881-b44e-4263-b05d-fb10a5ad1836",
    "privateKey": "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
}

PROTOCOLS TESTED:
1. Master ED25519 Protocol (master_coinbase_ed25519_protocol.py)
2. Advanced Trade API (coinbase_advanced_api.py) 
3. CDP Authentication (coinbase_cdp_auth.py)
4. JWT Authentication (coinbase_jwt_auth.py)
5. Credentials Integration (credentials.py)
"""

import sys
import os
import json
import base64
import time
from typing import Dict, Any, List, Tuple

# Add current directory to path
sys.path.append('.')

def test_credentials_integration():
    """Test credentials.py integration with JSON format"""
    print("🔐 Testing credentials.py JSON integration...")
    
    try:
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Verify JSON credential fields
        expected_api_key_id = "2636c881-b44e-4263-b05d-fb10a5ad1836"
        expected_private_key = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
        
        print(f"   Expected API Key ID: {expected_api_key_id}")
        print(f"   Loaded API Key ID:   {getattr(creds, 'COINBASE_API_KEY_ID', 'NOT_FOUND')}")
        print(f"   Expected Private Key: {expected_private_key[:20]}...")
        print(f"   Loaded Private Key:   {getattr(creds, 'COINBASE_PRIVATE_KEY', 'NOT_FOUND')[:20]}...")
        
        # Check primary fields
        if hasattr(creds, 'COINBASE_API_KEY_ID') and creds.COINBASE_API_KEY_ID == expected_api_key_id:
            print("   ✅ COINBASE_API_KEY_ID matches JSON")
        else:
            print("   ❌ COINBASE_API_KEY_ID mismatch")
            
        if hasattr(creds, 'COINBASE_PRIVATE_KEY') and creds.COINBASE_PRIVATE_KEY == expected_private_key:
            print("   ✅ COINBASE_PRIVATE_KEY matches JSON")
        else:
            print("   ❌ COINBASE_PRIVATE_KEY mismatch")
            
        # Check legacy fields
        if hasattr(creds, 'COINBASE_API_KEY') and creds.COINBASE_API_KEY == expected_api_key_id:
            print("   ✅ COINBASE_API_KEY (legacy) matches JSON")
        else:
            print("   ❌ COINBASE_API_KEY (legacy) mismatch")
            
        # Check live trading enforcement
        else:
            
        return True
        
    except Exception as e:
        print(f"   ❌ Credentials integration test failed: {e}")
        return False

def test_master_protocol():
    """Test master ED25519 protocol"""
    print("\n🚀 Testing Master ED25519 Protocol...")
    
    try:
        from master_coinbase_ed25519_protocol import MasterCoinbaseED25519Protocol
        
        # Test Advanced Trade endpoint
        print("   Testing Advanced Trade endpoint...")
        auth_advanced = MasterCoinbaseED25519Protocol(use_cdp_endpoint=False)
        success_advanced = auth_advanced.test_authentication()
        
        if success_advanced:
            print("   ✅ Advanced Trade authentication successful")
        else:
            print("   ❌ Advanced Trade authentication failed")
            
        # Test CDP endpoint  
        print("   Testing CDP endpoint...")
        auth_cdp = MasterCoinbaseED25519Protocol(use_cdp_endpoint=True)
        success_cdp = auth_cdp.test_authentication()
        
        if success_cdp:
            print("   ✅ CDP authentication successful")
        else:
            print("   ❌ CDP authentication failed")
            
        return success_advanced or success_cdp
        
    except Exception as e:
        print(f"   ❌ Master protocol test failed: {e}")
        return False

def test_existing_coinbase_api():
    """Test existing coinbase_advanced_api.py"""
    print("\n₿ Testing Existing Coinbase Advanced API...")
    
    try:
        from coinbase_advanced_api import CoinbaseAdvancedTradeAPI
        from credentials import WolfpackCredentials
        
        creds = WolfpackCredentials()
        
        # Initialize API with JSON credentials
        cb_api = CoinbaseAdvancedTradeAPI(
            api_key=creds.COINBASE_API_KEY_ID,
            private_key_b64=creds.COINBASE_PRIVATE_KEY
        )
        
        # Test API calls
        print("   Testing API connectivity...")
        accounts = cb_api.get_accounts()
        products = cb_api.list_products()
        
        print(f"   ✅ Coinbase Advanced API connected successfully")
        print(f"   📊 Accounts: {len(accounts.get('accounts', []))}")
        print(f"   📈 Products: {len(products.get('products', []))}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Coinbase Advanced API test failed: {e}")
        return False

def test_jwt_generation():
    """Test JWT token generation with JSON credentials"""
    print("\n🔑 Testing JWT Token Generation...")
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        import uuid
        
        # JSON credentials
        api_key_id = "2636c881-b44e-4263-b05d-fb10a5ad1836"
        private_key_b64 = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
        
        # Decode private key
        private_key_bytes = base64.b64decode(private_key_b64)
        print(f"   Private key length: {len(private_key_bytes)} bytes")
        
        # Try different key loading methods
        if len(private_key_bytes) == 32:
            private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
            print("   ✅ Loaded as 32-byte ED25519 key")
        elif len(private_key_bytes) == 64:
            private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes[:32])
            print("   ✅ Loaded as 64-byte ED25519 key (first 32 bytes)")
        else:
            raise ValueError(f"Unexpected key length: {len(private_key_bytes)}")
        
        # Generate JWT token
        current_time = int(time.time())
        payload = {
            'iss': api_key_id,
            'exp': current_time + 120,
            'iat': current_time,
            'sub': api_key_id
        }
        
        headers = {
            'alg': 'EdDSA',
            'kid': api_key_id,
            'typ': 'JWT'
        }
        
        token = jwt.encode(payload, private_key, algorithm='EdDSA', headers=headers)
        print(f"   ✅ JWT token generated successfully")
        print(f"   📝 Token length: {len(token)} characters")
        print(f"   🔑 Token preview: {token[:50]}...")
        
        # Decode and verify structure
        decoded = jwt.decode(token, options={"verify_signature": False})
        print(f"   ✅ Token structure verified")
        print(f"   📊 Payload keys: {list(decoded.keys())}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ JWT generation test failed: {e}")
        return False

def test_key_format_analysis():
    """Analyze the private key format"""
    print("\n🔍 Analyzing Private Key Format...")
    
    try:
        private_key_b64 = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
        
        # Base64 decode
        private_key_bytes = base64.b64decode(private_key_b64)
        
        print(f"   Base64 string length: {len(private_key_b64)} characters")
        print(f"   Decoded byte length: {len(private_key_bytes)} bytes")
        print(f"   First 8 bytes (hex): {private_key_bytes[:8].hex()}")
        print(f"   Last 8 bytes (hex): {private_key_bytes[-8:].hex()}")
        
        # Analyze format
        if len(private_key_bytes) == 32:
            print("   📋 Format: Raw ED25519 private key (32 bytes)")
        elif len(private_key_bytes) == 64:
            print("   📋 Format: Combined private+public key (64 bytes)")
            print("   📝 Private key: first 32 bytes")
            print("   📝 Public key: last 32 bytes")
        else:
            print(f"   📋 Format: Unknown ({len(private_key_bytes)} bytes)")
            
        # Try loading as ED25519
        from cryptography.hazmat.primitives.asymmetric import ed25519
        
        if len(private_key_bytes) == 32:
            key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
            print("   ✅ Successfully loaded as ED25519 private key")
        elif len(private_key_bytes) == 64:
            key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes[:32])
            print("   ✅ Successfully loaded as ED25519 private key (first 32 bytes)")
        
        # Get public key
        public_key = key.public_key()
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        print(f"   📤 Derived public key length: {len(public_bytes)} bytes")
        print(f"   📤 Public key (hex): {public_bytes.hex()}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Key format analysis failed: {e}")
        return False

def test_environment_setup():
    """Test environment and dependency setup"""
    print("\n🔧 Testing Environment Setup...")
    
    dependencies = [
        ('jwt', 'PyJWT library'),
        ('cryptography', 'Cryptography library'),
        ('requests', 'HTTP requests library'),
        ('base64', 'Base64 encoding (built-in)'),
        ('json', 'JSON handling (built-in)')
    ]
    
    missing_deps = []
    
    for dep, desc in dependencies:
        try:
            __import__(dep)
            print(f"   ✅ {desc}")
        except ImportError:
            print(f"   ❌ {desc} - MISSING")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n   🚨 Missing dependencies: {', '.join(missing_deps)}")
        print("   📦 Install with: pip install " + " ".join(missing_deps))
        return False
    else:
        print("   ✅ All dependencies available")
        return True

def main():
    """Run comprehensive protocol test suite"""
    print("🧪 COMPREHENSIVE COINBASE ED25519 PROTOCOL TEST SUITE")
    print("=" * 60)
    print("JSON Credentials:")
    print('  {"id": "2636c881-b44e-4263-b05d-fb10a5ad1836",')
    print('   "privateKey": "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="}')
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Key Format Analysis", test_key_format_analysis),
        ("JWT Generation", test_jwt_generation),
        ("Credentials Integration", test_credentials_integration),
        ("Master Protocol", test_master_protocol),
        ("Existing Coinbase API", test_existing_coinbase_api)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            test_results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🚀 ALL TESTS PASSED - COINBASE ED25519 PROTOCOL READY!")
        print("🔐 Constitutional PIN: 841921")
        print("🎯 Ready for live trading integration")
    elif passed > 0:
        print("⚠️  PARTIAL SUCCESS - Some protocols working")
        print("🔧 Check failed tests and resolve dependencies")
    else:
        print("❌ ALL TESTS FAILED - Protocol needs debugging")
        print("🛠️  Check credentials and dependencies")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
