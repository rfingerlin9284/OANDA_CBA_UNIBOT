IS_LIVE_MODE = True

REQUIRE_OCO = True

REQUIRE_COINBASE_API = True

if not IS_LIVE_MODE:

    raise RuntimeError("�� LIVE_MODE is not active. Execution blocked.")


#!/usr/bin/env python3
"""
🔐 COINBASE ADVANCED TRADE API WITH JWT ED25519
LIVE TRADING ONLY - NO live_mode/live_mode MODE
Hamilton, NJ EST/EDT timezone aware
"""

import time
import json
import base64
import uuid
from datetime import datetime, timedelta
import requests
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import pytz

class CoinbaseAdvancedTradeAPI:
    """
    🚀 Coinbase Advanced Trade API with JWT ED25519 Authentication
    Constitutional PIN: 841921 - Live Trading Only
    """
    """🔥 Coinbase Advanced Trade API with JWT ed25519 authentication"""
    
    def __init__(self, api_key, private_key_b64):
        """
        Initialize Coinbase Advanced Trade API
        
        Args:
            api_key: Your Coinbase API key name
            private_key_b64: Your base64-encoded ed25519 private key
        """
        self.api_key = api_key
        self.private_key_b64 = private_key_b64
        self.base_url = "https://api.coinbase.com"  # LIVE ENDPOINT
        
        # Hamilton, NJ timezone
        self.local_tz = pytz.timezone('America/New_York')  # EST/EDT
        
        # Decode private key
        self.private_key = self._load_private_key()
        
        print("🔐 Coinbase Advanced Trade API initialized (LIVE)")
        print(f"🌍 Local timezone: {self.local_tz}")
        
    def _load_private_key(self):
        """Load ed25519 private key from base64 raw bytes"""
        try:
            # Decode base64 private key (should be 32 bytes for ED25519)
            private_key_bytes = base64.b64decode(self.private_key_b64)
            
            if len(private_key_bytes) != 32:
                raise Exception(f"ED25519 private key must be exactly 32 bytes, got {len(private_key_bytes)}")
            
            # Create ED25519 private key from raw bytes
            private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
            
            return private_key
            
        except Exception as e:
            raise Exception(f"Failed to load ED25519 private key: {e}")
    
    def _create_jwt_token(self, request_method, request_path, body=""):
        """Create JWT token with ED25519 signature protocol for Coinbase Advanced Trade"""
        
        # Current timestamp
        timestamp = int(time.time())
        
        # JWT payload for Coinbase Advanced Trade
        payload = {
            'iss': 'cdp',  # Coinbase Developer Platform
            'nbf': timestamp,
            'exp': timestamp + 120,  # 2 minutes expiration
            'sub': self.api_key,
            'uri': request_method.upper() + ' ' + self.base_url + request_path,
        }
        
        # Sign with ED25519 private key using proper signature protocol
        token = jwt.encode(
            payload,
            self.private_key,
            algorithm='EdDSA',  # ED25519 signature algorithm
            headers={'kid': self.api_key, 'nonce': str(uuid.uuid4())}
        )
        
        return token
    
    def _make_request(self, method, endpoint, params=None, data=None):
        """Make authenticated request to Coinbase Advanced Trade API"""
        
        url = f"{self.base_url}{endpoint}"
        
        # Prepare body
        body = ""
        if data:
            body = json.dumps(data)
        
        # Create JWT token
        jwt_token = self._create_jwt_token(method, endpoint, body)
        
        # Headers
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        
        # Make request
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Coinbase API request failed: {e}")
    
    def get_accounts(self):
        """Get portfolio accounts"""
        return self._make_request('GET', '/api/v3/brokerage/accounts')
    
    def get_account(self, account_uuid):
        """Get specific account details"""
        return self._make_request('GET', f'/api/v3/brokerage/accounts/{account_uuid}')
    
    def list_products(self):
        """List available trading products (spot pairs)"""
        return self._make_request('GET', '/api/v3/brokerage/market/products')
    
    def get_product(self, product_id):
        """Get specific product details"""
        return self._make_request('GET', f'/api/v3/brokerage/market/products/{product_id}')
    
    def get_product_candles(self, product_id, start_time, end_time, granularity='FIVE_MINUTE'):
        """Get historical candles for a product"""
        params = {
            'start': start_time,
            'end': end_time,
            'granularity': granularity
        }
        return self._make_request('GET', f'/api/v3/brokerage/market/products/{product_id}/candles', params=params)
    
    def create_order(self, client_order_id, product_id, side, order_configuration):
        """Create a new order"""
        data = {
            'client_order_id': client_order_id,
            'product_id': product_id,
            'side': side,
            'order_configuration': order_configuration
        }
        return self._make_request('POST', '/api/v3/brokerage/orders', data=data)
    
    def list_orders(self, product_id=None, order_status=None, limit=100):
        """List orders"""
        params = {'limit': limit}
        if product_id:
            params['product_id'] = product_id
        if order_status:
            params['order_status'] = order_status
            
        return self._make_request('GET', '/api/v3/brokerage/orders/historical/batch', params=params)
    
    def get_order(self, order_id):
        """Get specific order details"""
        return self._make_request('GET', f'/api/v3/brokerage/orders/historical/{order_id}')
    
    def cancel_orders(self, order_ids):
        """Cancel multiple orders"""
        data = {'order_ids': order_ids}
        return self._make_request('POST', '/api/v3/brokerage/orders/batch_cancel', data=data)
    
    def get_portfolios(self):
        """Get portfolios"""
        return self._make_request('GET', '/api/v3/brokerage/portfolios')
    
    def get_market_time_info(self):
        """Get current market time and session info"""
        now_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
        now_local = now_utc.astimezone(self.local_tz)
        
        # Market session detection
        hour_local = now_local.hour
        
        session_info = {
            'current_time_utc': now_utc.isoformat(),
            'current_time_local': now_local.isoformat(),
            'local_timezone': str(self.local_tz),
            'weekday': now_local.weekday(),  # 0=Monday, 6=Sunday
            'is_weekend': now_local.weekday() >= 5,
        }
        
        # Market sessions (approximate times in ET)
        if 3 <= hour_local < 8:
            session_info['active_session'] = 'Asian (Tokyo/Hong Kong)'
        elif 8 <= hour_local < 12:
            session_info['active_session'] = 'London (overlap with Asian)'
        elif 8 <= hour_local < 17:
            session_info['active_session'] = 'London/New York'
        elif 9 <= hour_local < 17:
            session_info['active_session'] = 'New York'
        else:
            session_info['active_session'] = 'After hours/Asian prep'
        
        return session_info
    
    def create_spot_market_buy(self, product_id, quote_size):
        """Create spot market buy order"""
        client_order_id = f"wolfpack_buy_{int(time.time())}"
        order_config = {
            'market_market_ioc': {
                'quote_size': str(quote_size)
            }
        }
        return self.create_order(client_order_id, product_id, 'BUY', order_config)
    
    def create_spot_market_sell(self, product_id, base_size):
        """Create spot market sell order"""
        client_order_id = f"wolfpack_sell_{int(time.time())}"
        order_config = {
            'market_market_ioc': {
                'base_size': str(base_size)
            }
        }
        return self.create_order(client_order_id, product_id, 'SELL', order_config)
    
    def create_spot_limit_buy(self, product_id, base_size, limit_price):
        """Create spot limit buy order"""
        client_order_id = f"wolfpack_limit_buy_{int(time.time())}"
        order_config = {
            'limit_limit_gtc': {
                'base_size': str(base_size),
                'limit_price': str(limit_price)
            }
        }
        return self.create_order(client_order_id, product_id, 'BUY', order_config)
    
    def create_spot_limit_sell(self, product_id, base_size, limit_price):
        """Create spot limit sell order"""
        client_order_id = f"wolfpack_limit_sell_{int(time.time())}"
        order_config = {
            'limit_limit_gtc': {
                'base_size': str(base_size),
                'limit_price': str(limit_price)
            }
        }
        return self.create_order(client_order_id, product_id, 'SELL', order_config)


    """Test Coinbase Advanced Trade API with ed25519"""
    
    # You need to replace these with your actual credentials
    API_KEY = "YOUR_COINBASE_API_KEY_NAME"  # Your API key name
    PRIVATE_KEY_B64 = "YOUR_BASE64_ENCODED_ED25519_PRIVATE_KEY"  # Your base64 private key
    
    try:
        # Initialize API
        cb_api = CoinbaseAdvancedTradeAPI(API_KEY, PRIVATE_KEY_B64)
        
        print("\n🎯 Testing Coinbase Advanced Trade API...")
        
        # Test market time
        market_info = cb_api.get_market_time_info()
        print(f"📅 Market time info: {market_info}")
        
        # Test products (this should work even without valid credentials for basic info)
        # products = cb_api.list_products()
        # print(f"📊 Available products: {len(products.get('products', []))}")
        
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Make sure you have valid Coinbase Advanced Trade API credentials")

if __name__ == "__main__":
