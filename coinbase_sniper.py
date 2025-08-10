"""
COINBASE SPOT CRYPTO SNIPER - LIVE TRADING ONLY
REAL MONEY AT RISK - NO live_mode/PRACTICE MODE

Scans 8 most liquid crypto spot pairs for FVG setups
Uses LIVE Coinbase Advanced Trade API
NO PERPS/MARGIN - SPOT TRADING ONLY
"""

import time
import ccxt
from datetime import datetime, timezone
import logging
from typing import Dict, List, Optional

# Import our modules
from fvg_strategy import FVGStrategy
from credentials import WolfpackCredentials
from executor import TradeExecutor
from logger import log_signal, log_error, log_trade
from capital_manager import capital_manager
from emergency_bail import record_trade_result, is_bailout_triggered
from pair_selection import is_pair_blocked, block_pair


class CoinbaseSniper:
    """Coinbase Spot Crypto FVG Sniper - LIVE TRADING ONLY"""
    
    def __init__(self):
        print("🚀 Initializing Coinbase Spot FVG Sniper...")
        print("🚨 LIVE TRADING MODE - REAL MONEY AT RISK!")
        print("💰 SPOT TRADING ONLY - NO PERPS/MARGIN")
        
        # Load credentials
        self.creds = WolfpackCredentials()
        
        # Initialize LIVE Coinbase API
        self.exchange = ccxt.coinbase({
            'apiKey': self.creds.COINBASE_API_KEY,
            'secret': self.creds.COINBASE_SECRET,
            'password': self.creds.COINBASE_PASSPHRASE,
            'ssl': True,
            'live_mode': False,  # LIVE TRADING ONLY
            'urls': {
                'api': 'https://api.coinbase.com',  # LIVE ENDPOINT
            }
        })
        
        # Initialize strategy and executor
        self.strategy = FVGStrategy()
        self.executor = TradeExecutor("COINBASE")
        
        # Track active trades (max 1 per pair)
        self.active_trades = set()
        
        # Coinbase spot crypto pairs (8 most liquid)
        self.pairs = [
            "BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD",
            "DOT/USD", "AVAX/USD", "MATIC/USD", "LINK/USD"
        ]
        
        print(f"📊 Monitoring {len(self.pairs)} LIVE crypto spot pairs")
        print(f"🎯 Min confidence: {self.strategy.MIN_CONFIDENCE}")
        print(f"💰 Risk per trade: {self.creds.RISK_PER_TRADE}%")
        
    def get_candles(self, pair: str, count: int = 50) -> List[Dict]:
        try:
            # Fetch OHLCV data (timestamp, open, high, low, close, volume)
            ohlcv = self.exchange.fetch_ohlcv(
                symbol=pair,
                timeframe='5m',  # 5-minute candles
                limit=count
            )
            
            candles = []
            for candle in ohlcv:
                candles.append({
                    'timestamp': candle[0] / 1000,  # Convert to seconds
                    'open': candle[1],
                    'high': candle[2],
                    'low': candle[3],
                    'close': candle[4],
                    'volume': candle[5]
                })
            
            return candles
            
        except Exception as e:
            log_error(f"Failed to get Coinbase candles for {pair}: {e}", "COINBASE_API")
            return []
    
    def check_account_status(self) -> bool:
        """Check LIVE Coinbase account status"""
        try:
            balance = self.exchange.fetch_balance()
            
            usd_balance = balance.get('USD', {}).get('free', 0)
            total_balance = balance.get('USD', {}).get('total', 0)
            
            print(f"💰 LIVE USD Balance: ${usd_balance:.2f}")
            print(f"📊 Total USD: ${total_balance:.2f}")
            
            # Check if account is healthy for trading
            if usd_balance < 50:  # Minimum balance check
                log_error("LIVE Coinbase USD balance too low for trading", "COINBASE_ACCOUNT")
                return False
                
            # Show other significant balances
            for asset, info in balance.items():
                if asset != 'USD' and info.get('total', 0) > 0:
                    print(f"   {asset}: {info['total']:.6f}")
                
            return True
            
        except Exception as e:
            log_error(f"Failed to check LIVE Coinbase account: {e}", "COINBASE_ACCOUNT")
            return False
    
    def scan_pair(self, pair: str) -> Optional[Dict]:
        """Scan single pair for FVG signals"""
        try:
            # Emergency bail: skip all trading if triggered
            if is_bailout_triggered():
                print("⛔ Bailout active — system locked. Skipping all trades.")
                return None
            # Drift guard: block pairs on cooldown
            if is_pair_blocked(pair):
                print(f"⛔ {pair} blocked (cooldown active)")
                return None
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
            log_error(f"Error scanning {pair}: {e}", "COINBASE_SCAN")
            return None
    
    def execute_signal(self, signal: Dict) -> bool:
        """Execute FVG signal with OCO-like order"""
        try:
            pair = signal['pair']
            print(f"\n🎯 EXECUTING {signal['setup_type']} on {pair}")
            print(f"   Direction: {signal['direction']}")
            print(f"   Entry: ${signal['entry']:.2f}")
            print(f"   SL: ${signal['sl']:.2f}")
            print(f"   TP: ${signal['tp']:.2f}")
            print(f"   Confidence: {signal['confidence']}")
            print(f"   Gap Size: {signal['gap_size']}%")
            # Calculate position size based on capital and risk
            stop_dist = abs(signal['entry'] - signal['sl'])
            risk_amt = capital_manager.get() * 0.01  # 1% risk
            size = risk_amt / stop_dist if stop_dist > 0 else 0
            # Execute trade with OCO-like logic
            success = self.executor.execute_oco_trade(
                pair=pair,
                direction=signal['direction'],
                entry=signal['entry'],
                sl=signal['sl'],
                tp=signal['tp'],
                confidence=signal['confidence'],
                size=size
            )
            if success:
                self.active_trades.add(pair)
                log_trade(f"Crypto FVG trade executed: {signal['direction']} {pair}", pair)
                print(f"✅ Spot crypto trade executed successfully on {pair}")
                return True
            else:
                log_error(f"Failed to execute crypto FVG trade on {pair}", "TRADE_EXECUTION")
                print(f"❌ Spot crypto trade execution failed on {pair}")
                block_pair(pair)  # Block pair after failed trade
                return False
        except Exception as e:
            log_error(f"Error executing signal: {e}", "TRADE_EXECUTION")
            return False
    
    def update_active_trades(self):
        """Update status of active trades and remove completed ones"""
        try:
            # Get current open orders from Coinbase
            open_orders = self.exchange.fetch_open_orders()
            current_trade_pairs = set()
            for order in open_orders:
                symbol = order['symbol']
                current_trade_pairs.add(symbol)
            # Remove pairs that no longer have active trades
            completed_trades = self.active_trades - current_trade_pairs
            for pair in completed_trades:
                self.active_trades.remove(pair)
                # Simulate P&L for capital and bail logic (replace with real P&L logic)
                import random
                win = random.choice([True, False])
                pnl = 30 if win else -30
                capital_manager.update(pnl)
                record_trade_result(win)
                if not win:
                    block_pair(pair)
                print(f"✅ Crypto trade completed on {pair} - pair available for new signals")
        except Exception as e:
            log_error(f"Error updating active crypto trades: {e}", "TRADE_UPDATE")
    
    def run_scanner(self):
        """Main scanner loop for LIVE Coinbase spot trading"""
        print("\n" + "="*60)
        print("🚀 STARTING COINBASE SPOT FVG SNIPER - LIVE TRADING")
        print("🚨 REAL MONEY AT RISK - NO live_mode MODE")
        print("💰 SPOT TRADING ONLY - NO PERPS/MARGIN")
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
                
                print(f"\n🔍 Crypto Scan #{scan_count} at {current_time}")
                print(f"📊 Active crypto trades: {len(self.active_trades)}")
                
                # Update active trades status
                self.update_active_trades()
                
                # Scan all pairs for signals
                signals_found = 0
                for pair in self.pairs:
                    signal = self.scan_pair(pair)
                    
                    if signal:
                        signals_found += 1
                        print(f"🎯 Crypto FVG signal found on {pair}!")
                        
                        # Execute the signal
                        if self.execute_signal(signal):
                            print(f"✅ Crypto signal executed on {pair}")
                        else:
                            print(f"❌ Crypto signal execution failed on {pair}")
                
                if signals_found == 0:
                    print("🔍 No crypto FVG signals found this scan")
                
                # Check account every 10 scans
                if scan_count % 10 == 0:
                    if not self.check_account_status():
                        print("❌ Crypto account issue detected - stopping scanner")
                        break
                
                # Wait before next scan (12 seconds to avoid rate limits)
                time.sleep(12)
                
        except KeyboardInterrupt:
            print("\n🛑 Crypto scanner stopped by user")
        except Exception as e:
            log_error(f"Crypto scanner crashed: {e}", "SCANNER_ERROR")
            print(f"💥 Crypto scanner crashed: {e}")
        
        print("\n🚀 Coinbase Spot FVG Sniper stopped")


def main():
    """Start Coinbase spot FVG sniper"""
    sniper = CoinbaseSniper()
    sniper.run_scanner()


if __name__ == "__main__":
    main()
