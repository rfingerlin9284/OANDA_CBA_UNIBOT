#!/bin/bash
# patch_coinbase_api_sdk.sh: Create SDK-based Coinbase API wrapper
cat > coinbase_advanced_api_sdk.py << 'EOF'
#!/usr/bin/env python3
"""
🔥 COINBASE ADVANCED TRADE API WRAPPER WITH OFFICIAL SDK
Wrapper around official coinbase-advanced-py SDK for swarm integration
"""

import sys
import time
from datetime import datetime

try:
    from coinbase.rest import RESTClient
    from coinbase.websocket import WSClient
except ImportError as e:
    print(f"❌ Coinbase SDK not installed: {e}")
    print("Install with: pip install coinbase-advanced-py")
    sys.exit(1)

class CoinbaseAdvancedAPI:
    """🔥 Coinbase Advanced Trade API using official SDK"""
    
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        
        # Initialize REST client
        self.client = RESTClient(
            api_key=self.api_key,
            api_secret=self.api_secret
        )
        
        print(f"🔐 Coinbase Advanced Trade SDK initialized")
        print(f"    API Key: {self.api_key}")
        print(f"    Using official coinbase-advanced-py SDK")

    def get_accounts(self):
        """Get all accounts"""
        try:
            response = self.client.get_accounts()
            return response
        except Exception as e:
            print(f"❌ get_accounts error: {e}")
            return None

    def list_products(self):
        """List all products"""
        try:
            response = self.client.get_products()
            return response
        except Exception as e:
            print(f"❌ list_products error: {e}")
            return None

    def get_product(self, product_id):
        """Get specific product"""
        try:
            response = self.client.get_product(product_id)
            return response
        except Exception as e:
            print(f"❌ get_product error: {e}")
            return None

    def create_market_order(self, product_id, side, size):
        """Create market order"""
        try:
            # Build order configuration
            order_config = {
                "market_market_ioc": {
                    "quote_size" if side.lower() == "buy" else "base_size": str(size)
                }
            }
            
            response = self.client.create_order(
                client_order_id=f"wolfpack_{int(time.time())}",
                product_id=product_id,
                side=side.upper(),
                order_configuration=order_config
            )
            return response
        except Exception as e:
            print(f"❌ create_market_order error: {e}")
            return None

    def create_limit_order(self, product_id, side, size, price):
        """Create limit order"""
        try:
            # Build order configuration
            order_config = {
                "limit_limit_gtc": {
                    "base_size": str(size),
                    "limit_price": str(price)
                }
            }
            
            response = self.client.create_order(
                client_order_id=f"wolfpack_limit_{int(time.time())}",
                product_id=product_id,
                side=side.upper(),
                order_configuration=order_config
            )
            return response
        except Exception as e:
            print(f"❌ create_limit_order error: {e}")
            return None

    def get_orders(self, product_id=None):
        """Get orders"""
        try:
            response = self.client.list_orders(
                product_id=product_id,
                order_status="OPEN"
            )
            return response
        except Exception as e:
            print(f"❌ get_orders error: {e}")
            return None

    def cancel_orders(self, order_ids):
        """Cancel orders"""
        try:
            response = self.client.cancel_orders(order_ids=order_ids)
            return response
        except Exception as e:
            print(f"❌ cancel_orders error: {e}")
            return None

    def get_candles(self, product_id, start_time, end_time, granularity="FIVE_MINUTE"):
        """Get candles/OHLC data"""
        try:
            response = self.client.get_candles(
                product_id=product_id,
                start=start_time,
                end=end_time,
                granularity=granularity
            )
            return response
        except Exception as e:
            print(f"❌ get_candles error: {e}")
            return None

    """Test the Coinbase API wrapper"""
    print("🧪 TESTING COINBASE API WRAPPER...")
    
    # Import credentials
    sys.path.append('.')
    from credentials import WolfpackCredentials
    
    creds = WolfpackCredentials()
    
    # Initialize wrapper
    cb_api = CoinbaseAdvancedAPI(
        api_key=creds.COINBASE_API_KEY,
        api_secret=creds.COINBASE_API_SECRET
    )
    
    # Test accounts
    print("\n📊 Testing accounts...")
    accounts = cb_api.get_accounts()
    if accounts:
        print("✅ Accounts working")
    else:
        print("❌ Accounts failed")
    
    # Test products
    print("\n📊 Testing products...")
    products = cb_api.list_products()
    if products:
        print("✅ Products working")
    else:
        print("❌ Products failed")
    
    # Test specific product
    print("\n📊 Testing BTC-USD product...")
    btc_product = cb_api.get_product("BTC-USD")
    if btc_product:
        print("✅ BTC-USD product working")
    else:
        print("❌ BTC-USD product failed")
    

if __name__ == "__main__":
EOF

echo "[✅] coinbase_advanced_api_sdk.py created with official SDK wrapper."
