#!/usr/bin/env python3
"""
🔌 Coinbase Advanced API Connection Test
Constitutional PIN: 841921
Standalone connection verification for RBOTzilla Elite 18+18
"""

import logging
import sys
import os

# Setup logging
logging.basicConfig(filename='logs/system_health.log', level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

    """Test Coinbase Advanced API connection"""
    print("🔌 Testing Coinbase Advanced API Connection...")
    print("🔐 Constitutional PIN: 841921")
    print("-" * 50)
    
    try:
        # Import credentials
        sys.path.append('/home/ing/overlord/wolfpack-lite/oanda_cba_unibot')
        from credentials import WolfpackCredentials
        
        creds = WolfpackCredentials()
        print("✅ Credentials loaded successfully")
        
        # Check if we have Coinbase credentials
        if not hasattr(creds, 'COINBASE_API_KEY') or not creds.COINBASE_API_KEY:
            print("❌ COINBASE_API_KEY not found in credentials")
            logging.error("❌ COINBASE_API_KEY missing")
            return False
            
        if not hasattr(creds, 'COINBASE_API_SECRET') or not creds.COINBASE_API_SECRET:
            print("❌ COINBASE_API_SECRET not found in credentials")  
            logging.error("❌ COINBASE_API_SECRET missing")
            return False
            
        print("✅ Coinbase credentials found")
        
        # Try to import coinbase SDK
        try:
            from coinbase.wallet.client import Client
            print("✅ Coinbase SDK imported successfully")
            
            # Test connection
            client = Client(
                creds.COINBASE_API_KEY,
                creds.COINBASE_API_SECRET
            )
            
            # Get accounts
            accounts = client.get_accounts()
            if accounts and accounts.data:
                account = accounts.data[0]
                print(f"✅ COINBASE CONNECTION SUCCESS!")
                print(f"💰 Account: {account.name} Currency: {account.currency} Balance: {account.balance}")
                logging.info("✅ COINBASE CONNECTION SUCCESS")
                return True
            else:
                print("⚠️ Connected but no account data returned")
                logging.warning("⚠️ Connected but no account data")
                return False
                
        except ImportError as e2:
            print(f"❌ Failed to import Coinbase libraries: {e2}")
            print("🔧 Installing coinbase SDK...")
            
            # Try to install the package
            import subprocess
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "coinbase"])
                print("✅ coinbase SDK installed successfully")
                return False
            except subprocess.CalledProcessError as install_error:
                print(f"❌ Failed to install coinbase SDK: {install_error}")
                logging.error(f"❌ Coinbase installation failed: {install_error}")
                return False
            
    except Exception as e:
        print(f"❌ COINBASE CONNECTION FAILED: {e}")
        logging.error(f"❌ COINBASE CONNECTION FAILED: {e}")
        return False

def main():
    print("=" * 60)
    print("🔌 COINBASE API CONNECTION TEST")
    print("=" * 60)
    
    
    if success:
        print("\n🎯 RESULT: COINBASE API READY FOR DEPLOYMENT")
        print("🔐 Constitutional PIN 841921 - CONNECTION VERIFIED")
    else:
        print("\n⚠️ RESULT: COINBASE API NEEDS ATTENTION")
        print("🔧 Check credentials and API setup")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    main()
