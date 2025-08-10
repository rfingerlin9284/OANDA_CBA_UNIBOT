#!/bin/bash
# fix_coinbase_api.sh: Update Coinbase API handler
cat > coinbase_advanced_api_fixed.py << 'EOF'
"""
🔥 COINBASE ADVANCED TRADE API WITH PROPER ED25519 JWT
Fixed implementation for proper authentication
"""

import jwt
import time
import json
import uuid
import base64
import requests
from cryptography.hazmat.primitives.asymmetric import ed25519
from datetime import datetime, timezone

class CoinbaseAdvancedAPI:
    """🔥 Coinbase Advanced Trade API with proper ED25519 JWT authentication"""
    
    def __init__(self, api_key, private_key_b64, api_url="https://api.coinbase.com"):
        self.api_key = api_key
        self.api_url = api_url
        
        # Load ED25519 private key from base64
        private_key_bytes = base64.b64decode(private_key_b64)
        if len(private_key_bytes) == 64:
            # Take first 32 bytes if key is 64 bytes
            private_key_bytes = private_key_bytes[:32]
        elif len(private_key_bytes) != 32:
            raise ValueError(f"ED25519 private key must be 32 bytes, got {len(private_key_bytes)}")
            
        self.private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
        
        print(f"🔐 Coinbase Advanced Trade API initialized")
        print(f"    API Key: {self.api_key}")
        print(f"    Base URL: {self.api_url}")

    def generate_jwt(self, method, path):
        """Generate JWT token with ED25519 signature"""
        timestamp = int(time.time())
        nonce = str(uuid.uuid4()).replace('-', '')
        
        payload = {
            "iss": "cdp",
            "nbf": timestamp,
            "exp": timestamp + 120,
            "sub": self.api_key,
            "uri": f"{method.upper()} {path}"
        }
        
        # Create JWT with ED25519 signature
        token = jwt.encode(
            payload,
            self.private_key,
            algorithm='EdDSA',
            headers={
                'kid': self.api_key,
                'nonce': nonce
            }
        )
        
        return token

    def _make_request(self, method, path, params=None, data=None):
        """Make authenticated request to Coinbase API"""
        jwt_token = self.generate_jwt(method, path)
        
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
            "User-Agent": "WolfpackLite/1.0"
        }
        
        url = f"{self.api_url}{path}"
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        return response

    def get_accounts(self):
        """Get all accounts"""
        response = self._make_request('GET', '/api/v3/brokerage/accounts')
        return response.json() if response.status_code == 200 else None

    def list_products(self):
        """List all products"""
        response = self._make_request('GET', '/api/v3/brokerage/products')
        return response.json() if response.status_code == 200 else None

    def get_product(self, product_id):
        """Get specific product"""
        response = self._make_request('GET', f'/api/v3/brokerage/products/{product_id}')
        return response.json() if response.status_code == 200 else None

    def create_order(self, client_order_id, product_id, side, order_configuration):
        """Create an order"""
        data = {
            "client_order_id": client_order_id,
            "product_id": product_id,
            "side": side,
            "order_configuration": order_configuration
        }
        
        response = self._make_request('POST', '/api/v3/brokerage/orders', data=data)
        return response.json() if response.status_code in [200, 201] else None

    def list_orders(self, product_id=None, order_status=None, limit=100):
        """List orders"""
        params = {"limit": limit}
        if product_id:
            params["product_id"] = product_id
        if order_status:
            params["order_status"] = order_status
            
        response = self._make_request('GET', '/api/v3/brokerage/orders/historical/batch', params=params)
        return response.json() if response.status_code == 200 else None

    def cancel_orders(self, order_ids):
        """Cancel orders"""
        data = {"order_ids": order_ids}
        response = self._make_request('POST', '/api/v3/brokerage/orders/batch_cancel', data=data)
        return response.json() if response.status_code == 200 else None

    """Test the Coinbase API"""
    print("🧪 TESTING COINBASE ADVANCED API...")
    
    # Load credentials
    api_key = "2636c881-b44e-4263-b05d-fb10a5ad1836"
    
    # Load raw key
    try:
        with open('ed25519_raw.key', 'r') as f:
            private_key_b64 = f.read().strip()
    except FileNotFoundError:
        print("❌ ed25519_raw.key not found. Run generate_ed25519_key.sh first.")
        return False
    
    # Initialize API
    cb_api = CoinbaseAdvancedAPI(api_key, private_key_b64)
    
    # Test accounts
    accounts = cb_api.get_accounts()
    if accounts:
        print(f"✅ Accounts: {len(accounts.get('accounts', []))} found")
    else:
        print("❌ Failed to get accounts")
        return False
    
    # Test products
    products = cb_api.list_products()
    if products:
        print(f"✅ Products: {len(products.get('products', []))} found")
    else:
        print("❌ Failed to get products")
        return False
    
    return True

if __name__ == "__main__":
EOF

echo "[✅] coinbase_advanced_api_fixed.py created."
