#!/usr/bin/env python3
"""
🚀 ED25519 COINBASE AUTHENTICATION SYSTEM
Constitutional PIN: 841921

COMPLETE ED25519 INTEGRATION:
✅ Ed25519 JWT generation (NOT ECDSA)
✅ Advanced Trading API support
✅ CDP SDK API support
✅ Color-coded responses
✅ Live trading integration
"""

import base64
import json
import time
import hmac
import hashlib
import secrets
from typing import Dict, Any, Optional, Union
from urllib.parse import urlparse
import requests
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder
from datetime import datetime
from typing import Dict, Optional, Any
import nacl.signing
import nacl.encoding


class Ed25519CoinbaseAuth:
    """
    🔐 ED25519 AUTHENTICATION FOR COINBASE APIs
    
    Supports both Advanced Trading and CDP SDK endpoints
    """
    
    def __init__(self, api_key: str, secret_key: str):
        """
        Initialize Ed25519 authentication
        
        Args:
            api_key: Coinbase API key ID
            secret_key: Ed25519 private key (base64 encoded)
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.key_name = api_key  # Use API key as key name
        
        # Ed25519 requires 32-byte seed, but Coinbase provides 64-byte key
        # Use first 32 bytes as the seed for Ed25519
        try:
            key_bytes = base64.b64decode(secret_key)
            if len(key_bytes) == 64:
                # Use first 32 bytes as the seed
                seed = key_bytes[:32]
            elif len(key_bytes) == 32:
                # Already a 32-byte seed
                seed = key_bytes
            else:
                raise ValueError(f"Invalid key length: {len(key_bytes)} bytes")
                
            self.signing_key = SigningKey(seed)
            print(f"� Ed25519 authentication initialized successfully")
            
        except Exception as e:
            raise ValueError(f"Failed to initialize Ed25519 key: {e}")
    
    def get_headers(self, method: str, path: str, body: str = "") -> Dict[str, str]:
        """
        Generate authentication headers for Coinbase Advanced Trading API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path  
            body: Request body (for POST requests)
            
        Returns:
            Dictionary of authentication headers
        """
        timestamp = str(int(time.time()))
        
        # Create message to sign
        message = timestamp + method.upper() + path + body
        
        # Sign with Ed25519
        signature = self.signing_key.sign(
            message.encode(),
            encoder=nacl.encoding.RawEncoder
        ).signature
        
        # Encode signature as base64
        signature_b64 = base64.b64encode(signature).decode()
        
        # Return headers
        headers = {
            "CB-ACCESS-KEY": self.api_key,
            "CB-ACCESS-SIGN": signature_b64,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "UNIBOT-Ed25519/1.0"
        }
        
        return headers

    def generate_jwt(self, method: str, host: str, path: str) -> str:
        """
        Generate Ed25519 JWT for Coinbase API authentication
        
        Args:
            method: HTTP method (GET, POST, etc.)
            host: API host (api.coinbase.com, api.cdp.coinbase.com)
            path: API endpoint path
            
        Returns:
            JWT token string
        """
        # Create header
        header = {
            "typ": "JWT",
            "alg": "EdDSA",  # Ed25519 algorithm
            "kid": self.key_name,
            "nonce": str(int(time.time()))
        }
        
        # Create payload
        uri = f"{method} {host}{path}"
        now = int(time.time())
        
        payload = {
            "iss": "cdp",
            "sub": self.key_name,
            "aud": ["cdp_service"],
            "nbf": now,
            "exp": now + 120,  # 2 minutes expiry
            "uri": uri
        }
        
        # Encode header and payload
        header_b64 = base64.urlsafe_b64encode(
            json.dumps(header, separators=(',', ':')).encode()
        ).decode().rstrip('=')
        
        payload_b64 = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(',', ':')).encode()
        ).decode().rstrip('=')
        
        # Create message to sign
        message = f"{header_b64}.{payload_b64}"
        
        # Sign with Ed25519
        signature = self.signing_key.sign(
            message.encode(),
            encoder=nacl.encoding.RawEncoder
        ).signature
        
        # Encode signature
        signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        # Return complete JWT
        jwt_token = f"{message}.{signature_b64}"
        
        print(f"🔐 Generated Ed25519 JWT: {jwt_token[:50]}...")
        return jwt_token
    
    def make_request(self, method: str, url: str, data: Optional[Dict] = None) -> Dict:
        """
        Make authenticated request to Coinbase API
        
        Args:
            method: HTTP method
            url: Full API URL
            data: Request payload (for POST requests)
            
        Returns:
            API response dictionary
        """
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        host = parsed.netloc
        path = parsed.path
        if parsed.query:
            path += f"?{parsed.query}"
        
        # Generate JWT
        jwt_token = self.generate_jwt(method, host, path)
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "UNIBOT-Ed25519/1.0"
        }
        
        # Make request
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            else:
                response = requests.request(method, url, headers=headers, json=data, timeout=30)
            
            # Parse response
            if response.headers.get('content-type', '').startswith('application/json'):
                return {
                    'status_code': response.status_code,
                    'success': response.status_code < 400,
                    'data': response.json() if response.text else {},
                    'headers': dict(response.headers)
                }
            else:
                return {
                    'status_code': response.status_code,
                    'success': response.status_code < 400,
                    'data': response.text,
                    'headers': dict(response.headers)
                }
                
        except Exception as e:
            return {
                'status_code': 0,
                'success': False,
                'error': str(e),
                'data': {}
            }


class ColorCodedCoinbaseAPI:
    """
    🎨 COLOR-CODED COINBASE API CLIENT
    
    Provides color-coded output for all API responses
    """
    
    def __init__(self, api_key: str, secret_key: str):
        self.auth = Ed25519CoinbaseAuth(api_key, secret_key)
        
        # Color codes
        self.colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'reset': '\033[0m'
        }
    
    def color_print(self, message: str, color: str = 'white'):
        """Print colored message"""
        print(f"{self.colors.get(color, '')}{message}{self.colors['reset']}")
    
    def format_response(self, response: Dict, api_type: str = "COINBASE"):
        """Format and color-code API response"""
        
        if api_type == "COINBASE":
            color = 'cyan'
            symbol = '₿'
        else:
            color = 'yellow'
            symbol = '💱'
        
        self.color_print(f"\n{symbol} {api_type} API RESPONSE:", color)
        self.color_print("=" * 50, color)
        
        if response['success']:
            self.color_print(f"✅ Status: {response['status_code']} SUCCESS", 'green')
            
            # Format data based on endpoint
            data = response.get('data', {})
            
            if 'accounts' in data:
                self.color_print("💰 ACCOUNT BALANCES:", 'green')
                for account in data['accounts'][:5]:  # Show first 5
                    currency = account.get('currency', 'Unknown')
                    balance = account.get('available_balance', {}).get('value', '0')
                    self.color_print(f"   {currency}: {balance}", 'white')
                    
            elif 'products' in data:
                self.color_print("📊 TRADING PRODUCTS:", 'blue')
                for product in data['products'][:5]:  # Show first 5
                    product_id = product.get('product_id', 'Unknown')
                    status = product.get('status', 'Unknown')
                    self.color_print(f"   {product_id}: {status}", 'white')
                    
            elif 'orders' in data:
                self.color_print("📋 ORDERS:", 'magenta')
                for order in data['orders'][:3]:  # Show first 3
                    order_id = order.get('order_id', 'Unknown')
                    side = order.get('side', 'Unknown')
                    status = order.get('status', 'Unknown')
                    self.color_print(f"   {order_id}: {side} {status}", 'white')
                    
            elif 'wallets' in data:
                self.color_print("👛 CDP WALLETS:", 'blue')
                for wallet in data['wallets'][:3]:  # Show first 3
                    wallet_id = wallet.get('id', 'Unknown')
                    network = wallet.get('network_id', 'Unknown')
                    self.color_print(f"   {wallet_id}: {network}", 'white')
                    
            else:
                # Generic data display
                self.color_print("📄 RESPONSE DATA:", 'white')
                if isinstance(data, dict):
                    for key, value in list(data.items())[:5]:
                        self.color_print(f"   {key}: {str(value)[:50]}...", 'white')
                else:
                    self.color_print(f"   {str(data)[:100]}...", 'white')
        else:
            self.color_print(f"❌ Status: {response['status_code']} FAILED", 'red')
            if 'error' in response:
                self.color_print(f"Error: {response['error']}", 'red')
    
    # Advanced Trading API Methods
    def get_accounts(self):
        """Get account balances"""
        self.color_print("🔍 Fetching Coinbase accounts...", 'cyan')
        response = self.auth.make_request(
            "GET", 
            "https://api.coinbase.com/api/v3/brokerage/accounts"
        )
        self.format_response(response, "COINBASE")
        return response
    
    def get_products(self):
        """Get trading products"""
        self.color_print("🔍 Fetching trading products...", 'cyan')
        response = self.auth.make_request(
            "GET",
            "https://api.coinbase.com/api/v3/brokerage/products"
        )
        self.format_response(response, "COINBASE")
        return response
    
    def get_orders(self):
        """Get order history"""
        self.color_print("🔍 Fetching order history...", 'cyan')
        response = self.auth.make_request(
            "GET",
            "https://api.coinbase.com/api/v3/brokerage/orders/historical/batch"
        )
        self.format_response(response, "COINBASE")
        return response
    
    def create_order(self, product_id: str, side: str, size: str, price: Optional[str] = None):
        """Create a new order"""
        self.color_print(f"📝 Creating {side} order for {product_id}...", 'cyan')
        
        order_data = {
            "client_order_id": f"unibot_{int(time.time())}",
            "product_id": product_id,
            "side": side.upper(),
            "order_configuration": {}
        }
        
        if price:
            # Limit order
            order_data["order_configuration"]["limit_limit_gtc"] = {
                "base_size": size,
                "limit_price": price
            }
        else:
            # Market order
            order_data["order_configuration"]["market_market_ioc"] = {
                "base_size": size
            }
        
        response = self.auth.make_request(
            "POST",
            "https://api.coinbase.com/api/v3/brokerage/orders",
            order_data
        )
        self.format_response(response, "COINBASE")
        return response
    
    # CDP SDK API Methods
    def create_wallet(self, network_id: str = "base-sepolia"):
        """Create CDP wallet"""
        self.color_print(f"👛 Creating CDP wallet on {network_id}...", 'blue')
        
        wallet_data = {
            "wallet": {
                "network_id": network_id,
                "user_server_signer": True
            }
        }
        
        response = self.auth.make_request(
            "POST",
            "https://api.cdp.coinbase.com/platform/v1/wallets",
            wallet_data
        )
        self.format_response(response, "CDP")
        return response
    
    def list_wallets(self):
        """List CDP wallets"""
        self.color_print("🔍 Fetching CDP wallets...", 'blue')
        response = self.auth.make_request(
            "GET",
            "https://api.cdp.coinbase.com/platform/v1/wallets"
        )
        self.format_response(response, "CDP")
        return response
    
    def get_asset(self, network_id: str, asset_id: str):
        """Get asset information"""
        self.color_print(f"🔍 Fetching {asset_id} on {network_id}...", 'blue')
        response = self.auth.make_request(
            "GET",
            f"https://api.cdp.coinbase.com/platform/v1/networks/{network_id}/assets/{asset_id}"
        )
        self.format_response(response, "CDP")
        return response


def test_ed25519_apis():
    """Test all Ed25519 API endpoints"""
    
    print("🚀 TESTING ED25519 COINBASE APIS")
    print("🔐 Constitutional PIN: 841921")
    print("=" * 60)
    
    # Ed25519 API credentials
    API_KEY = "bbd70034-6acb-4c1c-8d7a-4358a434ed4b"
    SECRET_KEY = "yN8Q2bgm7bCGlLptrbixoGO+SIUu1cfyVyh/uTzk4BGXGzz1IrbEBBFJa+6dw4O3Ar4pkbWKW1SOeUB/r8n1kg=="
    
    api = ColorCodedCoinbaseAPI(API_KEY, SECRET_KEY)
    
    try:
        # Test Advanced Trading API
        api.color_print("🧪 TESTING ADVANCED TRADING API", 'cyan')
        api.get_accounts()
        time.sleep(1)
        
        api.get_products()
        time.sleep(1)
        
        api.get_orders()
        time.sleep(1)
        
        # Test CDP SDK API
        api.color_print("\n🧪 TESTING CDP SDK API", 'blue')
        api.list_wallets()
        time.sleep(1)
        
        api.get_asset("base-mainnet", "ETH")
        time.sleep(1)
        
        api.color_print("\n✅ ALL ED25519 TESTS COMPLETED", 'green')
        
    except Exception as e:
        api.color_print(f"❌ Test failed: {e}", 'red')


if __name__ == "__main__":
    test_ed25519_apis()
