#!/usr/bin/env python3
"""
🚀 TEST ORGANIZED MARKET DISPLAY WITH ED25519 COINBASE INTEGRATION
Constitutional PIN: 841921
Demonstrates organized format with both OANDA and Coinbase data
"""

import time
import json
from datetime import datetime
from organized_market_display import OrganizedMarketDisplay
from coinbase_ws_stream import CoinbaseWebSocketStream

def liveulate_live_data():
    display = OrganizedMarketDisplay()
    
    # Simulate OANDA tick data (using the same format as your logs)
    sample_oanda_ticks = [
        {
            'type': 'PRICE',
            'instrument': 'EUR_USD',
            'bids': [{'price': '1.16612', 'liquidity': 500000}],
            'asks': [{'price': '1.16627', 'liquidity': 500000}],
            'time': '2025-08-06T23:11:16.140685672Z',
            'tradeable': True
        },
        {
            'type': 'PRICE', 
            'instrument': 'USD_JPY',
            'bids': [{'price': '147.209', 'liquidity': 500000}],
            'asks': [{'price': '147.231', 'liquidity': 500000}],
            'time': '2025-08-06T23:11:16.045392864Z',
            'tradeable': True
        },
        {
            'type': 'PRICE',
            'instrument': 'GBP_USD', 
            'bids': [{'price': '1.33570', 'liquidity': 500000}],
            'asks': [{'price': '1.33594', 'liquidity': 500000}],
            'time': '2025-08-06T23:11:16.005784924Z',
            'tradeable': True
        },
        {
            'type': 'PRICE',
            'instrument': 'EUR_JPY',
            'bids': [{'price': '171.680', 'liquidity': 500000}],
            'asks': [{'price': '171.710', 'liquidity': 500000}],
            'time': '2025-08-06T23:11:13.548187113Z',
            'tradeable': True
        },
        {
            'type': 'PRICE',
            'instrument': 'GBP_JPY',
            'bids': [{'price': '196.645', 'liquidity': 500000}],
            'asks': [{'price': '196.689', 'liquidity': 500000}],
            'time': '2025-08-06T23:11:14.387054519Z',
            'tradeable': True
        }
    ]
    
    # Simulate Coinbase crypto data
    sample_coinbase_ticks = [
        {
            'product_id': 'BTC-USD',
            'price': 45234.56,
            'bid': 45230.12,
            'ask': 45238.99,
            'volume_24h': 1523456.78,
            'time': '2025-08-06T23:11:16.000000Z'
        },
        {
            'product_id': 'ETH-USD', 
            'price': 2834.67,
            'bid': 2834.12,
            'ask': 2835.22,
            'volume_24h': 8234567.89,
            'time': '2025-08-06T23:11:16.100000Z'
        },
        {
            'product_id': 'SOL-USD',
            'price': 25.43,
            'bid': 25.41,
            'ask': 25.45,
            'volume_24h': 2345678.90,
            'time': '2025-08-06T23:11:16.200000Z'
        },
        {
            'product_id': 'ADA-USD',
            'price': 0.4567,
            'bid': 0.4565,
            'ask': 0.4569,
            'volume_24h': 12345678.90,
            'time': '2025-08-06T23:11:16.300000Z'
        }
    ]
    
    print(f"🚀 STARTING ORGANIZED MARKET DISPLAY DEMONSTRATION")
    print(f"🔐 Constitutional PIN: 841921")
    print(f"📊 Will show organized format with both OANDA and Coinbase data")
    print(f"⏱️ Updates every 3 seconds. Press Ctrl+C to stop.")
    print(f"=" * 60)
    
    try:
        iteration = 0
        while True:
            # Update OANDA data
            for tick in sample_oanda_ticks:
                # Add some price variation
                variation = (iteration % 10) * 0.0001
                if tick['bids']:
                    original_bid = float(tick['bids'][0]['price'])
                    tick['bids'][0]['price'] = str(original_bid + variation)
                if tick['asks']:
                    original_ask = float(tick['asks'][0]['price'])  
                    tick['asks'][0]['price'] = str(original_ask + variation)
                
                display.update_oanda_tick(tick)
            
            # Update Coinbase data
            for tick in sample_coinbase_ticks:
                # Add some price variation
                variation_pct = (iteration % 20) * 0.001
                tick['price'] = tick['price'] * (1 + variation_pct)
                tick['bid'] = tick['bid'] * (1 + variation_pct)
                tick['ask'] = tick['ask'] * (1 + variation_pct)
                
                display.update_coinbase_tick(tick)
            
            # Display organized data
            display.display_organized_data()
            
            # Wait and update counter
            time.sleep(3)
            iteration += 1
            
    except KeyboardInterrupt:
        print(f"\n{display._colorize('👋 Organized Market Display Demo Stopped', 'yellow')}")
        print(f"🔐 Ready to integrate with live OANDA and Coinbase streams")

    """Test Coinbase ED25519 authentication"""
    print(f"\n🔐 TESTING COINBASE ED25519 JWT AUTHENTICATION")
    print(f"=" * 50)
    
    try:
        from working_coinbase_ed25519_auth import WorkingCoinbaseED25519Auth
        
        auth = WorkingCoinbaseED25519Auth()
        
        # Test JWT token generation
        jwt_token = auth.generate_jwt_token()
        if jwt_token:
            print(f"✅ JWT Token Generated Successfully")
            print(f"   Length: {len(jwt_token)} characters")
            print(f"   Algorithm: EdDSA (ED25519)")
            print(f"   API Key ID: {auth.api_key_id}")
            return True
        else:
            print(f"❌ Failed to generate JWT token")
            return False
            
    except ImportError as e:
        print(f"⚠️ Authentication module not available: {e}")
        return False
    except Exception as e:
        return False

if __name__ == "__main__":
    print(f"🚀 RBOTZILLA ELITE 18+18 - ORGANIZED MARKET DISPLAY TEST")
    print(f"🔐 Constitutional PIN: 841921")
    print(f"=" * 60)
    
    # Test authentication first
    
    if auth_success:
    else:
    
    input()
    
    liveulate_live_data()
