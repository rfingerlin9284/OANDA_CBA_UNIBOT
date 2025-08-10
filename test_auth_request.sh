#!/bin/bash
import requests
import json

print("🔧 TESTING COINBASE API AUTHENTICATION...")

try:
    # Load JWT token
    with open('coinbase_jwt.txt', 'r') as f:
        jwt_token = f.read().strip()
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
        "User-Agent": "WolfpackLite/1.0"
    }
    
    # Test accounts endpoint
    url = "https://api.coinbase.com/api/v3/brokerage/accounts"
    print(f"Testing endpoint: {url}")
    
    response = requests.get(url, headers=headers, timeout=10)
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        accounts = data.get('accounts', [])
        print(f"[✅] Coinbase API Auth Success!")
        print(f"    Found {len(accounts)} accounts")
        
        # Show account details
        for i, account in enumerate(accounts[:3]):  # Show first 3
            currency = account.get('currency', 'Unknown')
            balance = account.get('available_balance', {}).get('value', '0')
            print(f"    Account {i+1}: {currency} = {balance}")
            
    elif response.status_code == 401:
        print(f"[❌] Authentication Failed: 401 Unauthorized")
        print(f"    Response: {response.text}")
        
    elif response.status_code == 403:
        print(f"[❌] Permission Denied: 403 Forbidden")
        print(f"    Response: {response.text}")
        
    else:
        print(f"[⚠️] Unexpected Response: {response.status_code}")
        print(f"    Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"[❌] Request Error: {e}")
    
except Exception as e:
    print(f"[❌] General Error: {e}")
EOF

