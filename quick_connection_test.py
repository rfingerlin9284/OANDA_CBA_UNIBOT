#!/usr/bin/env python3
"""
🔥 RBOTzilla Elite 18+18 - Quick Connection Verification
Constitutional PIN: 841921
"""

from credentials import WolfpackCredentials
import oandapyV20
from oandapyV20.endpoints.accounts import AccountSummary

print("🔥 RBOTzilla Elite 18+18 Connection Test")
print("Constitutional PIN: 841921")
print("=" * 50)

try:
    print("🔐 Loading credentials...")
    creds = WolfpackCredentials()
    
    print("🔗 Connecting to Oanda Live API...")
    api = oandapyV20.API(
        access_token=creds.OANDA_API_KEY, 
        environment="live"
    )
    
    print("📊 Requesting account summary...")
    request = AccountSummary(creds.OANDA_ACCOUNT_ID)
    response = api.request(request)
    
    balance = response['account']['balance']
    currency = response['account']['currency']
    
    print("✅ CONNECTION SUCCESS!")
    print(f"💰 Account Balance: ${balance} {currency}")
    print("🚀 NEURAL LINKS: FULLY OPERATIONAL")
    print("💥 READY FOR LIVE DEPLOYMENT")
    print("🔥 Elite 18+18 system primed for market domination!")
    
except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
    print("🔧 Check credentials and network connection")
    
    if "401" in str(e):
        print("   🔑 AUTH ERROR: Invalid API key or Account ID")
    elif "503" in str(e):
        print("   🔧 SERVICE DOWN: Oanda outage")
    else:
        print("   🌐 NETWORK: Check internet connection")
