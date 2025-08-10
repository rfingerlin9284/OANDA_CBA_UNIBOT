#!/usr/bin/env python3
"""
📡 OANDA WebSocket Stream Handler - RBOTzilla Elite 18+18
Constitutional PIN: 841921
REAL LIVE STREAMING WITH ORGANIZED DISPLAY FORMAT
"""
import oandapyV20
import json
import logging
import time
from credentials import WolfpackCredentials
from organized_market_display import OrganizedMarketDisplay

class OandaWebSocketStream:
    def __init__(self):
        self.creds = WolfpackCredentials()
        self.api = oandapyV20.API(
            access_token=self.creds.OANDA_API_KEY,
            environment="live"
        )
        self.constitutional_pin = "841921"
        # Initialize organized display for REAL LIVE DATA
        self.display = OrganizedMarketDisplay()
        self.last_display_update = time.time()
        
    def start_price_stream(self, instruments=None):
        """Start real-time price streaming with organized display"""
        if instruments is None:
            # Elite 15 Forex Pairs - LIVE OANDA
            instruments = [
                "EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CHF", 
                "USD_CAD", "NZD_USD", "EUR_GBP", "EUR_JPY", "GBP_JPY", 
                "AUD_JPY", "CHF_JPY", "EUR_CHF", "GBP_AUD", "EUR_AUD"
            ]
        
        from oandapyV20.endpoints.pricing import PricingStream
        
        params = {"instruments": ",".join(instruments)}
        pricing = PricingStream(self.creds.OANDA_ACCOUNT_ID, params=params)
        
        print(f"🚀 Starting REAL LIVE OANDA Stream - Organized Display Format")
        print(f"📊 Streaming {len(instruments)} Elite Forex Pairs...")
        
        for tick in self.api.request(pricing):
            self.process_tick(tick)
                
    def process_tick(self, tick):
        """Process REAL LIVE tick data and update organized display"""
        # Update display with REAL LIVE OANDA data
        self.display.update_oanda_tick(tick)
        
        # Update display every 2 seconds for smooth viewing
        current_time = time.time()
        if current_time - self.last_display_update >= 2.0:
            self.display.display_organized_data()
            self.last_display_update = current_time

if __name__ == "__main__":
    print("🚀 REAL LIVE OANDA STREAMING - ORGANIZED FORMAT")
    print("📊 Converting chaotic tick stream to clean organized display...")
    try:
        stream = OandaWebSocketStream()
        stream.start_price_stream()
    except KeyboardInterrupt:
        print("\n👋 LIVE OANDA Organized Stream Stopped")
    except Exception as e:
        print(f"❌ Stream Error: {e}")
