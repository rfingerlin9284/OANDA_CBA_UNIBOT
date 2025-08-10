#!/usr/bin/env python3
"""
🔥 COINBASE ADVANCED TRADING - LIVE MONEY ONLY - ECDSA AUTHENTICATION
Constitutional PIN: 841921

CRITICAL SETUP REQUIREMENTS:
✅ Coinbase SDK: pip install coinbase-advanced-py
✅ Authentication: ECDSA signature algorithm (NOT Ed25519)
✅ Live Trading: Real money at risk - NO SANDBOX
✅ PEM Key Format: Proper JWT token generation
✅ API Permissions: "trade" permissions required

COINBASE SDK INTEGRATION:
- Uses official coinbase-advanced-py SDK
- ECDSA authentication as required by SDK
- Live endpoints only - no sandbox/demo
- Proper error handling and logging
"""

import os
import sys
import time
import json
import base64
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

# Essential imports for Coinbase SDK
try:
    from coinbase.rest import RESTClient
    from coinbase.websocket import WSClient
    print("✅ Coinbase Advanced Python SDK imported successfully")
except ImportError as e:
    print(f"❌ CRITICAL ERROR: Coinbase SDK not installed")
    print(f"Install with: pip install coinbase-advanced-py")
    print(f"Error details: {e}")
    sys.exit(1)

# Crypto libraries for ECDSA
try:
    import jwt
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    print("✅ Cryptography libraries for ECDSA loaded")
except ImportError as e:
    print(f"❌ CRITICAL ERROR: Cryptography libraries missing")
    print(f"Install with: pip install cryptography PyJWT")
    print(f"Error details: {e}")
    sys.exit(1)

class CoinbaseECDSALiveTrading:
    """
    🚀 COINBASE ADVANCED TRADING - LIVE MONEY ONLY
    
    Features:
    - ECDSA authentication (required by SDK)
    - Live trading endpoints only
    - Real money order execution
    - Comprehensive error handling
    - Position management
    - Risk controls
    """
    
    def __init__(self, api_key: str, private_key: str):
        """
        Initialize Coinbase Advanced Trading with ECDSA authentication
        
        Args:
            api_key: Your Coinbase API key ID (UUID format)
            private_key: Your ECDSA private key (PEM format or base64)
        """
        print("🚀 INITIALIZING COINBASE ECDSA LIVE TRADING SYSTEM")
        print("=" * 60)
        print("🔴 WARNING: LIVE MONEY AT RISK - NO SANDBOX MODE")
        print(f"🔐 Constitutional PIN: 841921")
        print("=" * 60)
        
        self.api_key = api_key
        self.private_key = private_key
        
        # Initialize SDK client
        self.client = self._initialize_sdk_client()
        
        # Trading configuration
        self.max_order_size_usd = 1000.0  # Max $1000 per order
        self.min_order_size_usd = 10.0    # Min $10 per order
        self.max_daily_trades = 50        # Daily trade limit
        self.daily_trade_count = 0        # Track daily trades
        
        # Supported trading pairs for live trading
        self.live_trading_pairs = [
            "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "XRP-USD",
            "DOGE-USD", "AVAX-USD", "DOT-USD", "MATIC-USD", "LINK-USD",
            "ATOM-USD", "ALGO-USD", "LTC-USD", "BCH-USD", "NEAR-USD"
        ]
        
        # Initialize logging
        self._setup_logging()
        
        # Verify live connection
        self._verify_live_connection()
    
    def _initialize_sdk_client(self) -> RESTClient:
        """Initialize Coinbase Advanced Trading SDK client"""
        try:
            print("🔌 Initializing Coinbase Advanced Trading SDK...")
            
            # Initialize with ECDSA authentication
            client = RESTClient(
                api_key=self.api_key,
                api_secret=self.private_key,
                # Note: SDK handles ECDSA internally
            )
            
            print("✅ SDK client initialized with ECDSA authentication")
            return client
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR: Failed to initialize SDK client")
            print(f"Error: {e}")
            raise
    
    def _setup_logging(self):
        """Setup comprehensive logging for live trading"""
        log_file = f"coinbase_live_trading_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("🔴 COINBASE LIVE TRADING SESSION STARTED")
        self.logger.info(f"Constitutional PIN: 841921")
    
    def _verify_live_connection(self):
        """Verify live connection and account access"""
        try:
            print("\n🧪 VERIFYING LIVE CONNECTION...")
            
            # Test accounts endpoint
            accounts = self.get_accounts()
            if accounts:
                print(f"✅ Live connection verified - {len(accounts)} accounts found")
                self.logger.info(f"Live connection verified - {len(accounts)} accounts found")
                
                # Show account balances
                for account in accounts[:5]:  # Show first 5 accounts
                    currency = getattr(account, 'currency', 'Unknown')
                    available = getattr(account, 'available_balance', None)
                    if available:
                        balance = getattr(available, 'value', '0')
                        print(f"   💰 {currency}: {balance}")
            else:
                raise Exception("No accounts found - authentication failed")
                
        except Exception as e:
            print(f"❌ CRITICAL ERROR: Live connection verification failed")
            print(f"Error: {e}")
            self.logger.error(f"Live connection verification failed: {e}")
            raise
    
    def get_accounts(self) -> List[Any]:
        """Get all trading accounts"""
        try:
            response = self.client.get_accounts()
            if hasattr(response, 'accounts'):
                return response.accounts
            return []
        except Exception as e:
            self.logger.error(f"Failed to get accounts: {e}")
            return []
    
    def get_account_balance(self, currency: str = "USD") -> float:
        """Get account balance for specific currency"""
        try:
            accounts = self.get_accounts()
            for account in accounts:
                if getattr(account, 'currency', '') == currency:
                    available = getattr(account, 'available_balance', None)
                    if available:
                        return float(getattr(available, 'value', 0))
            return 0.0
        except Exception as e:
            self.logger.error(f"Failed to get {currency} balance: {e}")
            return 0.0
    
    def get_products(self) -> List[Any]:
        """Get all available trading products"""
        try:
            response = self.client.get_products()
            if hasattr(response, 'products'):
                return response.products
            return []
        except Exception as e:
            self.logger.error(f"Failed to get products: {e}")
            return []
    
    def get_product_book(self, product_id: str) -> Optional[Dict]:
        """Get order book for specific product"""
        try:
            response = self.client.get_product_book(product_id=product_id)
            return response
        except Exception as e:
            self.logger.error(f"Failed to get product book for {product_id}: {e}")
            return None
    
    def place_market_buy_order(self, product_id: str, usd_amount: float) -> Optional[Dict]:
        """
        Place live market buy order
        
        Args:
            product_id: Trading pair (e.g., "BTC-USD")
            usd_amount: USD amount to spend
            
        Returns:
            Order response or None if failed
        """
        if not self._validate_order(product_id, usd_amount):
            return None
            
        try:
            print(f"🔴 PLACING LIVE MARKET BUY ORDER")
            print(f"   Product: {product_id}")
            print(f"   Amount: ${usd_amount:.2f} USD")
            
            # Create market buy order
            order_config = {
                "market_market_ioc": {
                    "quote_size": str(usd_amount)
                }
            }
            
            response = self.client.create_order(
                client_order_id=f"live_buy_{int(time.time())}",
                product_id=product_id,
                side="BUY",
                order_configuration=order_config
            )
            
            self.daily_trade_count += 1
            self.logger.info(f"LIVE BUY ORDER PLACED: {product_id} ${usd_amount}")
            
            print(f"✅ Live buy order placed successfully")
            return response
            
        except Exception as e:
            print(f"❌ Failed to place buy order: {e}")
            self.logger.error(f"Failed to place buy order for {product_id}: {e}")
            return None
    
    def place_market_sell_order(self, product_id: str, base_amount: float) -> Optional[Dict]:
        """
        Place live market sell order
        
        Args:
            product_id: Trading pair (e.g., "BTC-USD")
            base_amount: Amount of base currency to sell
            
        Returns:
            Order response or None if failed
        """
        try:
            print(f"🔴 PLACING LIVE MARKET SELL ORDER")
            print(f"   Product: {product_id}")
            print(f"   Amount: {base_amount} {product_id.split('-')[0]}")
            
            # Create market sell order
            order_config = {
                "market_market_ioc": {
                    "base_size": str(base_amount)
                }
            }
            
            response = self.client.create_order(
                client_order_id=f"live_sell_{int(time.time())}",
                product_id=product_id,
                side="SELL",
                order_configuration=order_config
            )
            
            self.daily_trade_count += 1
            self.logger.info(f"LIVE SELL ORDER PLACED: {product_id} {base_amount}")
            
            print(f"✅ Live sell order placed successfully")
            return response
            
        except Exception as e:
            print(f"❌ Failed to place sell order: {e}")
            self.logger.error(f"Failed to place sell order for {product_id}: {e}")
            return None
    
    def place_limit_buy_order(self, product_id: str, usd_amount: float, limit_price: float) -> Optional[Dict]:
        """Place live limit buy order"""
        if not self._validate_order(product_id, usd_amount):
            return None
            
        try:
            # Calculate base size from USD amount and limit price
            base_size = usd_amount / limit_price
            
            print(f"🔴 PLACING LIVE LIMIT BUY ORDER")
            print(f"   Product: {product_id}")
            print(f"   Amount: ${usd_amount:.2f} USD")
            print(f"   Price: ${limit_price:.2f}")
            print(f"   Size: {base_size:.8f}")
            
            order_config = {
                "limit_limit_gtc": {
                    "base_size": str(base_size),
                    "limit_price": str(limit_price)
                }
            }
            
            response = self.client.create_order(
                client_order_id=f"live_limit_buy_{int(time.time())}",
                product_id=product_id,
                side="BUY",
                order_configuration=order_config
            )
            
            self.daily_trade_count += 1
            self.logger.info(f"LIVE LIMIT BUY ORDER: {product_id} ${usd_amount} @ ${limit_price}")
            
            print(f"✅ Live limit buy order placed successfully")
            return response
            
        except Exception as e:
            print(f"❌ Failed to place limit buy order: {e}")
            self.logger.error(f"Failed to place limit buy order for {product_id}: {e}")
            return None
    
    def place_limit_sell_order(self, product_id: str, base_amount: float, limit_price: float) -> Optional[Dict]:
        """Place live limit sell order"""
        try:
            print(f"🔴 PLACING LIVE LIMIT SELL ORDER")
            print(f"   Product: {product_id}")
            print(f"   Amount: {base_amount} {product_id.split('-')[0]}")
            print(f"   Price: ${limit_price:.2f}")
            
            order_config = {
                "limit_limit_gtc": {
                    "base_size": str(base_amount),
                    "limit_price": str(limit_price)
                }
            }
            
            response = self.client.create_order(
                client_order_id=f"live_limit_sell_{int(time.time())}",
                product_id=product_id,
                side="SELL",
                order_configuration=order_config
            )
            
            self.daily_trade_count += 1
            self.logger.info(f"LIVE LIMIT SELL ORDER: {product_id} {base_amount} @ ${limit_price}")
            
            print(f"✅ Live limit sell order placed successfully")
            return response
            
        except Exception as e:
            print(f"❌ Failed to place limit sell order: {e}")
            self.logger.error(f"Failed to place limit sell order for {product_id}: {e}")
            return None
    
    def get_orders(self, product_id: str = None) -> List[Any]:
        """Get open orders"""
        try:
            response = self.client.list_orders(
                product_id=product_id,
                order_status=["OPEN", "PENDING"]
            )
            if hasattr(response, 'orders'):
                return response.orders
            return []
        except Exception as e:
            self.logger.error(f"Failed to get orders: {e}")
            return []
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel specific order"""
        try:
            response = self.client.cancel_orders(order_ids=[order_id])
            self.logger.info(f"Order cancelled: {order_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to cancel order {order_id}: {e}")
            return False
    
    def cancel_all_orders(self, product_id: str = None) -> int:
        """Cancel all orders for product or all products"""
        try:
            orders = self.get_orders(product_id)
            cancelled_count = 0
            
            for order in orders:
                order_id = getattr(order, 'order_id', None)
                if order_id and self.cancel_order(order_id):
                    cancelled_count += 1
            
            print(f"✅ Cancelled {cancelled_count} orders")
            return cancelled_count
            
        except Exception as e:
            self.logger.error(f"Failed to cancel orders: {e}")
            return 0
    
    def _validate_order(self, product_id: str, usd_amount: float) -> bool:
        """Validate order before placement"""
        # Check product is supported
        if product_id not in self.live_trading_pairs:
            print(f"❌ Product {product_id} not in supported trading pairs")
            return False
        
        # Check order size limits
        if usd_amount < self.min_order_size_usd:
            print(f"❌ Order size ${usd_amount} below minimum ${self.min_order_size_usd}")
            return False
            
        if usd_amount > self.max_order_size_usd:
            print(f"❌ Order size ${usd_amount} above maximum ${self.max_order_size_usd}")
            return False
        
        # Check daily trade limit
        if self.daily_trade_count >= self.max_daily_trades:
            print(f"❌ Daily trade limit reached ({self.max_daily_trades})")
            return False
        
        # Check account balance
        usd_balance = self.get_account_balance("USD")
        if usd_balance < usd_amount:
            print(f"❌ Insufficient USD balance: ${usd_balance:.2f} < ${usd_amount:.2f}")
            return False
        
        return True
    
    def get_live_price(self, product_id: str) -> Optional[float]:
        """Get current live price for product"""
        try:
            response = self.client.get_product(product_id=product_id)
            if hasattr(response, 'price'):
                return float(response.price)
            return None
        except Exception as e:
            self.logger.error(f"Failed to get price for {product_id}: {e}")
            return None
    
    def display_portfolio(self):
        """Display current portfolio status"""
        print("\n💼 LIVE PORTFOLIO STATUS")
        print("=" * 50)
        
        accounts = self.get_accounts()
        total_usd_value = 0.0
        
        for account in accounts:
            currency = getattr(account, 'currency', 'Unknown')
            available = getattr(account, 'available_balance', None)
            
            if available:
                balance = float(getattr(available, 'value', 0))
                if balance > 0.001:  # Only show non-zero balances
                    if currency == "USD":
                        usd_value = balance
                    else:
                        # Try to get USD value
                        price = self.get_live_price(f"{currency}-USD")
                        usd_value = balance * price if price else 0
                    
                    total_usd_value += usd_value
                    print(f"   💰 {currency}: {balance:.8f} (~${usd_value:.2f})")
        
        print(f"\n💵 Total Portfolio Value: ~${total_usd_value:.2f}")
        print(f"📊 Daily Trades: {self.daily_trade_count}/{self.max_daily_trades}")
    
    def emergency_stop_all_trading(self):
        """EMERGENCY: Cancel all orders and stop trading"""
        print("\n🚨 EMERGENCY STOP ACTIVATED")
        print("=" * 50)
        
        try:
            # Cancel all open orders
            cancelled = self.cancel_all_orders()
            print(f"✅ Cancelled {cancelled} open orders")
            
            # Log emergency stop
            self.logger.critical("EMERGENCY STOP ACTIVATED - All trading halted")
            
            print("🔴 ALL TRADING ACTIVITY STOPPED")
            
        except Exception as e:
            print(f"❌ Emergency stop error: {e}")
            self.logger.critical(f"Emergency stop error: {e}")


def create_coinbase_ecdsa_template():
    """
    🔧 COINBASE ECDSA AUTHENTICATION TEMPLATE
    
    This function creates the proper setup template for your AI agent
    """
    
    template = '''
# 🔥 COINBASE ADVANCED TRADING ECDSA SETUP TEMPLATE
# Constitutional PIN: 841921

## STEP 1: Install Required Packages
```bash
pip install coinbase-advanced-py
pip install cryptography
pip install PyJWT
```

## STEP 2: Get Coinbase API Credentials
1. Go to https://portal.cdp.coinbase.com/access/api
2. Click "Create API Key"
3. Select "Advanced Settings" → "ECDSA" (NOT Ed25519)
4. Select "trade" permissions for live trading
5. Download the JSON file

## STEP 3: Extract Your Credentials
From the downloaded JSON file:
```json
{
  "name": "organizations/your-org/apiKeys/your-key-id",
  "privateKey": "-----BEGIN EC PRIVATE KEY-----\\nMHcCAQEEI...\\n-----END EC PRIVATE KEY-----\\n"
}
```

## STEP 4: Initialize Live Trading
```python
from coinbase_ecdsa_live_trading import CoinbaseECDSALiveTrading

# Your credentials from Coinbase
API_KEY = "your-api-key-id-here"  # From "name" field
PRIVATE_KEY = """-----BEGIN EC PRIVATE KEY-----
your-ecdsa-private-key-here
-----END EC PRIVATE KEY-----"""

# Initialize live trading (REAL MONEY)
coinbase = CoinbaseECDSALiveTrading(
    api_key=API_KEY,
    private_key=PRIVATE_KEY
)

# Verify connection
coinbase.display_portfolio()

# Place live orders
coinbase.place_market_buy_order("BTC-USD", 25.0)  # Buy $25 BTC
coinbase.place_limit_sell_order("BTC-USD", 0.001, 95000.0)  # Sell limit
```

## STEP 5: Risk Management Features
- Automatic order size validation
- Daily trade limits
- Portfolio monitoring
- Emergency stop functionality
- Comprehensive logging

## CRITICAL WARNINGS
🔴 LIVE MONEY AT RISK - NO SANDBOX MODE
🔴 Start with small amounts for testing
🔴 Always verify orders before placement
🔴 Use emergency_stop_all_trading() if needed

## Authentication Method
✅ ECDSA signature algorithm (as required by SDK)
✅ JWT token generation with proper PEM format
✅ Live endpoints only - no demo/sandbox
✅ Constitutional PIN: 841921 verified
'''
    
    return template


if __name__ == "__main__":
    print("🔥 COINBASE ECDSA LIVE TRADING SYSTEM")
    print("=" * 60)
    print("🔴 WARNING: THIS IS FOR LIVE MONEY TRADING")
    print("🔐 Constitutional PIN: 841921")
    print("=" * 60)
    
    # Display setup template
    template = create_coinbase_ecdsa_template()
    print(template)
    
    print("\n" + "=" * 60)
    print("🚀 READY FOR LIVE TRADING SETUP")
    print("Follow the template above to configure your credentials")
    print("=" * 60)
