#!/usr/bin/env python3
"""
🎯 COINBASE ED25519 AUTHENTICATION - PRODUCTION READY
Constitutional PIN: 841921
LIVE TRADING ONLY - Based on WORKING Advanced Trade CDP Format

This class implements the CONFIRMED WORKING Ed25519 authentication protocol
that successfully connected to Coinbase Advanced Trade API.
"""

import os
import jwt
import time
import uuid
import requests
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import serialization

class CoinbaseEd25519Auth:
    """
    Production-ready Coinbase Ed25519 authentication using WORKING protocol
    Constitutional PIN: 841921 - LIVE TRADING ONLY
    """
    
    def __init__(self, credentials_instance=None):
        if credentials_instance:
            self.creds = credentials_instance  # Use instance directly, don't call it
        else:
            from credentials import WolfpackCredentials
            self.creds = WolfpackCredentials()  # This one is correct - creates new instance
        
        # Load Ed25519 private key from PEM format (CONFIRMED WORKING)
        self.private_key = serialization.load_pem_private_key(
            self.creds.COINBASE_PRIVATE_KEY_PEM.encode(),
            password=None
        )
        
        print("✅ Coinbase Ed25519 authentication initialized")
        print(f"📋 API Key: {self.creds.COINBASE_API_KEY_ID}")
        print(f"🔐 Algorithm: EdDSA (Ed25519)")
    
    def generate_jwt_token(self, method: str = "GET", path: str = "/api/v3/brokerage/accounts") -> str:
        """
        Generate JWT token using CONFIRMED WORKING Advanced Trade CDP Format
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            
        Returns:
            JWT token string
        """
        request_host = "api.coinbase.com"
        current_time = int(time.time())
        
        # WORKING payload format (Advanced Trade CDP Format)
        payload = {
            "iss": "cdp",  # CDP issuer (CONFIRMED WORKING)
            "nbf": current_time,
            "exp": current_time + 120,  # 2 minutes expiration
            "sub": self.creds.COINBASE_API_KEY_ID,
            "uri": f"{method.upper()} {request_host}{path}",
            "aud": ["cdp_service"]
        }
        
        # WORKING headers format
        headers = {
            "kid": self.creds.COINBASE_API_KEY_ID,
            "nonce": str(uuid.uuid4()),
            "typ": "JWT",
            "alg": "EdDSA"  # Ed25519 algorithm
        }
        
        # Generate JWT token
        jwt_token = jwt.encode(payload, self.private_key, algorithm="EdDSA", headers=headers)
        return jwt_token
    
    def get_auth_headers(self, method: str = "GET", path: str = "/api/v3/brokerage/accounts") -> Dict[str, str]:
        """
        Get authentication headers for API requests
        
        Args:
            method: HTTP method
            path: API endpoint path
            
        Returns:
            Dictionary of authentication headers
        """
        jwt_token = self.generate_jwt_token(method, path)
        
        return {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
    
    def make_authenticated_request(self, method: str, path: str, data: Optional[Dict] = None) -> requests.Response:
        """
        Make authenticated request to Coinbase Advanced Trade API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            data: Optional request data for POST/PUT
            
        Returns:
            requests.Response object
        """
        # Construct full URL
        url = f"{self.creds.COINBASE_LIVE_URL}{path}"
        
        # Get authentication headers
        headers = self.get_auth_headers(method, path)
        
        # Make request
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response
    
    def get_accounts(self) -> Dict[str, Any]:
        """
        Get trading accounts (CONFIRMED WORKING)
        
        Returns:
            Dictionary containing account information
        """
        response = self.make_authenticated_request("GET", "/api/v3/brokerage/accounts")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get accounts: {response.status_code} - {response.text}")
    
    def get_products(self) -> Dict[str, Any]:
        """
        Get available trading products
        
        Returns:
            Dictionary containing product information
        """
        response = self.make_authenticated_request("GET", "/api/v3/brokerage/products")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get products: {response.status_code} - {response.text}")
    
    def get_orders(self) -> Dict[str, Any]:
        """
        Get order history
        
        Returns:
            Dictionary containing order information
        """
        response = self.make_authenticated_request("GET", "/api/v3/brokerage/orders/historical/batch")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get orders: {response.status_code} - {response.text}")
    
    def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Place a trading order (LIVE TRADING)
        
        Args:
            order_data: Order parameters dictionary
            
        Returns:
            Dictionary containing order response
        """
        print("🚀 PLACING LIVE ORDER")
        print(f"📊 Order Data: {order_data}")
        
        response = self.make_authenticated_request("POST", "/api/v3/brokerage/orders", order_data)
        
        if response.status_code in [200, 201]:
            print("✅ Order placed successfully")
            return response.json()
        else:
            print(f"❌ Order placement failed: {response.status_code} - {response.text}")
            raise Exception(f"Failed to place order: {response.status_code} - {response.text}")
    
        """
        Test the Ed25519 authentication connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            accounts = self.get_accounts()
            account_count = len(accounts.get('accounts', []))
            
            print(f"📊 Found {account_count} accounts")
            
            return True
            
        except Exception as e:
            return False

    """Test the production Ed25519 authentication"""
    
    print("🎯 TESTING PRODUCTION Ed25519 AUTHENTICATION")
    print("Constitutional PIN: 841921")
    print("=" * 50)
    
    try:
        # Initialize authentication
        auth = CoinbaseEd25519Auth()
        
        # Test connection
            print("\n🎉 PRODUCTION Ed25519 AUTHENTICATION READY")
            print("🚀 Integration with trading system can proceed")
            
            # Get additional info
            try:
                products = auth.get_products()
                product_count = len(products.get('products', []))
                print(f"📊 Available products: {product_count}")
            except Exception as e:
                print(f"⚠️  Products endpoint error: {e}")
            
            return True
        else:
            print("\n❌ PRODUCTION AUTHENTICATION FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False

if __name__ == "__main__":
