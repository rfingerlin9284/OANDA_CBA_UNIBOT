"""
OANDA FOREX SNIPER - LIVE TRADING ONLY
REAL MONEY AT RISK - NO live_mode/PRACTICE MODE

Scans 12 most liquid forex pairs for FVG setups
Uses LIVE OANDA API with hardcoded credentials
"""

import time
import oandapyV20
from oandapyV20.endpoints.instruments import InstrumentsCandles
from oandapyV20.endpoints.accounts import AccountDetails
from datetime import datetime, timezone
import logging
from typing import Dict, List, Optional

# Import our modules
from fvg_strategy import FVGStrategy
from credentials import WolfpackCredentials
from executor import TradeExecutor
from logger import log_signal, log_error, log_trade


class OandaSniper:
    """OANDA Forex FVG Sniper - LIVE TRADING ONLY"""
    
    def __init__(self):
        print("🦅 Initializing OANDA FVG Sniper...")
        print("🚨 LIVE TRADING MODE - REAL MONEY AT RISK!")
        
        # Load credentials
        self.creds = WolfpackCredentials()
        
        # Initialize LIVE OANDA API
        self.api = oandapyV20.API(
            access_token=self.creds.OANDA_API_KEY,
            environment="live"  # LIVE TRADING ENVIRONMENT
        )
        
        # Initialize strategy and executor
        self.strategy = FVGStrategy()
        self.executor = TradeExecutor("OANDA")
        
        # Track active trades (max 1 per pair)
        self.active_trades = set()
        
        # OANDA forex pairs (12 most liquid)
        self.pairs = [
            "EUR_USD", "GBP_USD", "USD_JPY", "USD_CHF", 
            "AUD_USD", "USD_CAD", "NZD_USD", "EUR_GBP",
            "EUR_JPY", "GBP_JPY", "AUD_JPY", "EUR_AUD"
        ]
        
        print(f"📊 Monitoring {len(self.pairs)} LIVE forex pairs")
        print(f"🎯 Min confidence: {self.strategy.MIN_CONFIDENCE}")
        print(f"💰 Risk per trade: {self.creds.RISK_PER_TRADE}%")
        
    def get_candles(self, pair: str, count: int = 50) -> List[Dict]:
        try:
            params = {
                "count": count,
                "granularity": "M5",  # 5-minute candles
                "price": "M"  # Mid prices
            }
            
            request = InstrumentsCandles(instrument=pair, params=params)
            response = self.api.request(request)
            
            candles = []
            for candle in response['candles']:
                if candle['complete']:  # Only completed candles
                    candles.append({
                        'timestamp': candle['time'],
                        'open': float(candle['mid']['o']),
                        'high': float(candle['mid']['h']),
                        'low': float(candle['mid']['l']),
                        'close': float(candle['mid']['c']),
                        'volume': candle['volume']
                    })
            
            return candles
            
        except Exception as e:
            log_error(f"Failed to get OANDA candles for {pair}: {e}", "OANDA_API")
            return []
    
    def check_account_status(self) -> bool:
        """Check LIVE OANDA account status"""
        try:
            request = AccountDetails(self.creds.OANDA_ACCOUNT_ID)
            response = self.api.request(request)
            
            balance = float(response['account']['balance'])
            open_trades = len(response['account']['trades'])
            
            print(f"💰 LIVE Account Balance: {balance:.2f} {response['account']['currency']}")
            print(f"📊 Open Trades: {open_trades}")
            
            # Check if account is healthy
            if balance < 100:  # Minimum balance check
                log_error("LIVE account balance too low for trading", "OANDA_ACCOUNT")
                return False
                
            return True
            
        except Exception as e:
            log_error(f"Failed to check LIVE OANDA account: {e}", "OANDA_ACCOUNT")
            return False
    
    def scan_pair(self, pair: str) -> Optional[Dict]:
        """Scan single pair for FVG signals"""
        try:
            # Skip if already have active trade on this pair
            if pair in self.active_trades:
                return None
                
            # Get candles
            candles = self.get_candles(pair)
            if len(candles) < 25:
                return None
                
            # Scan for FVG signal
            signal = self.strategy.scan_for_signals(candles, pair)
            
            if signal and self.strategy.validate_setup(signal):
                log_signal(
                    pair, 
                    signal['direction'].lower(),
                    signal['confidence'],
                    {
                        'entry': signal['entry'],
                        'sl': signal['sl'], 
                        'tp': signal['tp'],
                        'gap_size': signal['gap_size'],
                        'setup_type': signal['setup_type']
                    }
                )
                return signal
                
            return None
            
        except Exception as e:
            log_error(f"Error scanning {pair}: {e}", "OANDA_SCAN")
            return None
    
    def execute_signal(self, signal: Dict) -> bool:
        """Execute FVG signal with OCO order"""
        try:
            pair = signal['pair']
            
            print(f"\n🎯 EXECUTING {signal['setup_type']} on {pair}")
            print(f"   Direction: {signal['direction']}")
            print(f"   Entry: {signal['entry']}")
            print(f"   SL: {signal['sl']}")
            print(f"   TP: {signal['tp']}")
            print(f"   Confidence: {signal['confidence']}")
            print(f"   Gap Size: {signal['gap_size']}%")
            
            # Execute trade with OCO
            success = self.executor.execute_oco_trade(
                pair=pair,
                direction=signal['direction'],
                entry=signal['entry'],
                sl=signal['sl'],
                tp=signal['tp'],
                confidence=signal['confidence']
            )
            
            if success:
                self.active_trades.add(pair)
                log_trade(f"FVG trade executed: {signal['direction']} {pair}", pair)
                print(f"✅ Trade executed successfully on {pair}")
                return True
            else:
                log_error(f"Failed to execute FVG trade on {pair}", "TRADE_EXECUTION")
                print(f"❌ Trade execution failed on {pair}")
                return False
                
        except Exception as e:
            log_error(f"Error executing signal: {e}", "TRADE_EXECUTION")
            return False
    
    def update_active_trades(self):
        """Update status of active trades and remove completed ones"""
        try:
            # Get current trades from OANDA
            request = AccountDetails(self.creds.OANDA_ACCOUNT_ID)
            response = self.api.request(request)
            
            current_trade_pairs = set()
            for trade in response['account']['trades']:
                instrument = trade['instrument']
                current_trade_pairs.add(instrument)
            
            # Remove pairs that no longer have active trades
            completed_trades = self.active_trades - current_trade_pairs
            for pair in completed_trades:
                self.active_trades.remove(pair)
                print(f"✅ Trade completed on {pair} - pair available for new signals")
                
        except Exception as e:
            log_error(f"Error updating active trades: {e}", "TRADE_UPDATE")
    
    def run_scanner(self):
        """Main scanner loop for LIVE OANDA trading"""
        print("\n" + "="*60)
        print("🦅 STARTING OANDA FVG SNIPER - LIVE TRADING")
        print("🚨 REAL MONEY AT RISK - NO live_mode MODE")
        print("="*60)
        
        # Check account status first
        if not self.check_account_status():
            print("❌ Account check failed - stopping scanner")
            return
        
        scan_count = 0
        
        try:
            while True:
                scan_count += 1
                current_time = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
                
                print(f"\n🔍 Scan #{scan_count} at {current_time}")
                print(f"📊 Active trades: {len(self.active_trades)}")
                
                # Update active trades status
                self.update_active_trades()
                
                # Scan all pairs for signals
                signals_found = 0
                for pair in self.pairs:
                    signal = self.scan_pair(pair)
                    
                    if signal:
                        signals_found += 1
                        print(f"🎯 FVG signal found on {pair}!")
                        
                        # Execute the signal
                        if self.execute_signal(signal):
                            print(f"✅ Signal executed on {pair}")
                        else:
                            print(f"❌ Signal execution failed on {pair}")
                
                if signals_found == 0:
                    print("🔍 No FVG signals found this scan")
                
                # Check account every 10 scans
                if scan_count % 10 == 0:
                    if not self.check_account_status():
                        print("❌ Account issue detected - stopping scanner")
                        break
                
                # Wait before next scan (10 seconds)
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n🛑 Scanner stopped by user")
        except Exception as e:
            log_error(f"Scanner crashed: {e}", "SCANNER_ERROR")
            print(f"💥 Scanner crashed: {e}")
        
        print("\n🦅 OANDA FVG Sniper stopped")


def main():
    """Start OANDA FVG sniper"""
    sniper = OandaSniper()
    sniper.run_scanner()


if __name__ == "__main__":
    main()
