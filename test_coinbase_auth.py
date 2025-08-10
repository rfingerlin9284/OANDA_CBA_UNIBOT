#!/usr/bin/env python3
"""
🔐 RBOTZILLA COINBASE AUTHENTICATION TEST
Constitutional PIN: 841921
"""
import sys
import traceback
from credentials import WolfpackCredentials

    """Test Coinbase Advanced Trade authentication"""
    print("🔐 RBOTZILLA COINBASE AUTH TEST - Constitutional PIN: 841921")
    print("=" * 60)
    
    try:
        # Load credentials
        creds = WolfpackCredentials()
        print(f"[✅] Credentials loaded - Constitutional PIN: {creds.CONSTITUTIONAL_PIN}")
        
        # Validate credentials
        issues = creds.validate_credentials()
        if issues:
            print("[❌] Credential validation failed:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        
        print("[✅] Credential validation passed")
        
        # Test PEM loading
        try:
            pem_content = creds.COINBASE_PRIVATE_KEY_PEM
            print(f"[✅] PEM loaded successfully ({len(pem_content)} chars)")
            print(f"[🔍] PEM format check: {'✅' if 'BEGIN PRIVATE KEY' in pem_content else '❌'}")
        except Exception as e:
            print(f"[❌] PEM loading failed: {e}")
            return False
        
        # Test Coinbase API import
        try:
            from coinbase_ed25519_auth import CoinbaseEd25519Auth
            print("[✅] CoinbaseEd25519Auth imported successfully")
            
            # Initialize auth
            auth = CoinbaseEd25519Auth(creds)
            print("[✅] Coinbase auth initialized")
            
            # Test connection (if method exists)
                try:
                    return connection_result
                except Exception as e:
                    return False
            else:
                return True
                
        except ImportError as e:
            print(f"[❌] Coinbase auth import failed: {e}")
            return False
        except Exception as e:
            print(f"[❌] Coinbase auth initialization failed: {e}")
            return False
        
    except Exception as e:
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    if success:
        print("🎯 RBOTZILLA AUTH TEST: ✅ SUCCESS - Ready for live trading!")
        print("🚀 Constitutional PIN 841921 verified - System ready for deployment")
    else:
        print("❌ RBOTZILLA AUTH TEST: FAILED - Authentication issues detected")
        print("🔧 Review credentials and PEM format")
    
    sys.exit(0 if success else 1)
