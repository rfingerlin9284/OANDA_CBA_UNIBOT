#!/usr/bin/env python3
"""
🚀 UNIBOT MASTER STRATEGY COORDINATOR
Constitutional PIN: 841921

UNIFIED 18+18 STRATEGY SYSTEM:
✅ FOREX: FVG (Fair Value Gap) Strategy - OANDA
✅ CRYPTO: Momentum Strategy - Coinbase  
✅ DUAL-EXCHANGE: Cross-pair arbitrage monitoring
✅ RISK MANAGEMENT: OCO protection and position sizing
✅ LIVE ONLY: No simulation mode whatsoever

This coordinates both strategies across both exchanges simultaneously.
"""

import sys
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Import both strategies
try:
    from fvg_strategy import FVGStrategy
    from crypto_momentum_strategy import CryptoMomentumStrategy
    from executor import TradeExecutor
except ImportError as e:
    print(f"❌ Strategy import failed: {e}")
    sys.exit(1)

logger = logging.getLogger(__name__)


class UnibotMasterStrategy:
    """
    🎯 MASTER STRATEGY COORDINATOR FOR UNIBOT
    
    Manages both FVG forex and momentum crypto strategies
    with unified risk management and execution
    """
    
    def __init__(self):
        print("🚀 INITIALIZING UNIBOT MASTER STRATEGY")
        print("🔐 Constitutional PIN: 841921")
        print("=" * 60)
        
        # Initialize strategies
        self.fvg_strategy = FVGStrategy()
        self.crypto_strategy = CryptoMomentumStrategy()
        self.executor = TradeExecutor("UNIFIED")  # Unified executor for both exchanges
        
        # Trading parameters
        self.max_concurrent_trades = 6  # 3 forex + 3 crypto max
        self.daily_trade_limit = 20
        self.current_trades = 0
        self.daily_trades = 0
        
        # Elite 18+18 pairs
        self.forex_pairs = [
            "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF",
            "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY", "AUD/JPY", "EUR/CHF",
            "GBP/CHF", "NZD/JPY", "CAD/JPY", "EUR/AUD", "GBP/AUD", "AUD/CAD"
        ]
        
        self.crypto_pairs = [
            "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "AVAX-USD", 
            "LINK-USD", "MATIC-USD", "DOT-USD", "UNI-USD", "LTC-USD", "BCH-USD",
            "NEAR-USD", "OP-USD", "APT-USD", "INJ-USD", "DOGE-USD", "XLM-USD"
        ]
        
        # Active signals tracking
        self.active_signals = {}
        self.executed_trades = {}
        
        print(f"✅ Forex Strategy: {len(self.forex_pairs)} pairs (FVG)")
        print(f"✅ Crypto Strategy: {len(self.crypto_pairs)} pairs (Momentum)")
        print(f"🎯 Max Concurrent: {self.max_concurrent_trades} trades")
        print(f"📊 Daily Limit: {self.daily_trade_limit} trades")
    
    def scan_forex_signals(self, candle_data: Dict) -> List[Dict]:
        """
        Scan all forex pairs for FVG signals
        
        Args:
            candle_data: Dict with pair -> candles mapping
            
        Returns:
            List of valid FVG signals
        """
        signals = []
        
        for pair in self.forex_pairs:
            if pair not in candle_data:
                continue
                
            try:
                candles = candle_data[pair]
                signal = self.fvg_strategy.scan_for_signals(candles, pair)
                
                if signal and self.fvg_strategy.validate_setup(signal):
                    signal['exchange'] = 'OANDA'
                    signal['strategy'] = 'FVG'
                    signals.append(signal)
                    
                    logger.info(f"🎯 FVG Signal: {pair} {signal['direction']} "
                              f"Confidence: {signal['confidence']}")
                    
            except Exception as e:
                logger.error(f"❌ FVG scan error for {pair}: {e}")
        
        return signals
    
    def scan_crypto_signals(self, candle_data: Dict) -> List[Dict]:
        """
        Scan all crypto pairs for momentum signals
        
        Args:
            candle_data: Dict with pair -> candles mapping
            
        Returns:
            List of valid momentum signals
        """
        signals = []
        
        for pair in self.crypto_pairs:
            if pair not in candle_data:
                continue
                
            try:
                candles = candle_data[pair]
                signal = self.crypto_strategy.scan_for_signals(candles, pair)
                
                if signal and self.crypto_strategy.validate_setup(signal):
                    signal['exchange'] = 'COINBASE'
                    signal['strategy'] = 'MOMENTUM'
                    signals.append(signal)
                    
                    logger.info(f"🚀 Momentum Signal: {pair} {signal['direction']} "
                              f"Confidence: {signal['confidence']}")
                    
            except Exception as e:
                logger.error(f"❌ Momentum scan error for {pair}: {e}")
        
        return signals
    
    def prioritize_signals(self, all_signals: List[Dict]) -> List[Dict]:
        """
        Prioritize signals based on:
        1. Confidence level (higher is better)
        2. Risk-reward ratio (higher is better) 
        3. Strategy type (diversification)
        4. Exchange balance (avoid concentration)
        """
        if not all_signals:
            return []
            
        # Sort by confidence (primary) and risk-reward (secondary)
        prioritized = sorted(all_signals, key=lambda s: (
            s['confidence'],
            s['reward'] / s['risk'] if s['risk'] > 0 else 0
        ), reverse=True)
        
        # Apply diversification filters
        selected = []
        forex_count = 0
        crypto_count = 0
        max_per_exchange = self.max_concurrent_trades // 2
        
        for signal in prioritized:
            # Check limits
            if len(selected) >= self.max_concurrent_trades:
                break
                
            if signal['exchange'] == 'OANDA' and forex_count >= max_per_exchange:
                continue
                
            if signal['exchange'] == 'COINBASE' and crypto_count >= max_per_exchange:
                continue
                
            # Check if we already have a signal for this pair
            if signal['pair'] in [s['pair'] for s in selected]:
                continue
                
            selected.append(signal)
            
            if signal['exchange'] == 'OANDA':
                forex_count += 1
            else:
                crypto_count += 1
        
        return selected
    
    def execute_signal(self, signal: Dict) -> bool:
        """
        Execute a trading signal through the appropriate exchange
        
        Args:
            signal: Signal dictionary with all trade parameters
            
        Returns:
            True if trade executed successfully, False otherwise
        """
        try:
            # Check daily limits
            if self.daily_trades >= self.daily_trade_limit:
                logger.warning(f"⚠️ Daily trade limit reached: {self.daily_trades}")
                return False
            
            # Check concurrent trade limits
            if self.current_trades >= self.max_concurrent_trades:
                logger.warning(f"⚠️ Concurrent trade limit reached: {self.current_trades}")
                return False
            
            # Execute through executor
            success = self.executor.execute_oco_trade(
                pair=signal['pair'],
                direction=signal['direction'],
                entry=signal['entry'],
                sl=signal['sl'],
                tp=signal['tp'],
                confidence=signal['confidence']
            )
            
            if success:
                # Track the trade
                trade_id = f"{signal['pair']}_{int(time.time())}"
                self.executed_trades[trade_id] = {
                    'signal': signal,
                    'execution_time': datetime.utcnow(),
                    'trade_id': trade_id,
                    'status': 'ACTIVE'
                }
                
                self.current_trades += 1
                self.daily_trades += 1
                
                logger.info(f"✅ Trade executed: {signal['strategy']} {signal['pair']} "
                          f"{signal['direction']} on {signal['exchange']}")
                
                print(f"🎯 TRADE EXECUTED - {signal['strategy']} STRATEGY")
                print(f"   Exchange: {signal['exchange']}")
                print(f"   Pair: {signal['pair']}")
                print(f"   Direction: {signal['direction']}")
                print(f"   Entry: {signal['entry']}")
                print(f"   Stop Loss: {signal['sl']}")
                print(f"   Take Profit: {signal['tp']}")
                print(f"   Confidence: {signal['confidence']}")
                print(f"   Risk:Reward = 1:{signal['reward']/signal['risk']:.1f}")
                
                return True
            else:
                logger.error(f"❌ Trade execution failed for {signal['pair']}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Signal execution error: {e}")
            return False
    
    def run_strategy_scan(self, forex_candles: Dict, crypto_candles: Dict) -> int:
        """
        Run complete strategy scan across both exchanges
        
        Args:
            forex_candles: OANDA candle data
            crypto_candles: Coinbase candle data
            
        Returns:
            Number of trades executed
        """
        trades_executed = 0
        
        try:
            print("🔍 SCANNING FOR TRADING OPPORTUNITIES...")
            
            # Scan both exchanges
            forex_signals = self.scan_forex_signals(forex_candles)
            crypto_signals = self.scan_crypto_signals(crypto_candles)
            
            all_signals = forex_signals + crypto_signals
            
            if not all_signals:
                logger.info("📊 No valid signals found this scan")
                return 0
            
            # Prioritize and filter signals
            priority_signals = self.prioritize_signals(all_signals)
            
            logger.info(f"🎯 Found {len(all_signals)} total signals, "
                       f"prioritized to {len(priority_signals)}")
            
            # Execute priority signals
            for signal in priority_signals:
                if self.execute_signal(signal):
                    trades_executed += 1
                    time.sleep(1)  # Brief delay between executions
                    
        except Exception as e:
            logger.error(f"❌ Strategy scan error: {e}")
        
        return trades_executed
    
    def get_strategy_status(self) -> Dict:
        """Get current strategy status"""
        return {
            'active_trades': self.current_trades,
            'daily_trades': self.daily_trades,
            'forex_pairs_monitored': len(self.forex_pairs),
            'crypto_pairs_monitored': len(self.crypto_pairs),
            'executed_trades_today': len(self.executed_trades),
            'strategies_active': ['FVG_FOREX', 'MOMENTUM_CRYPTO'],
            'max_concurrent': self.max_concurrent_trades,
            'daily_limit': self.daily_trade_limit
        }
    
    def display_status(self):
        """Display strategy status"""
        status = self.get_strategy_status()
        
        print("\\n📊 UNIBOT STRATEGY STATUS")
        print("=" * 40)
        print(f"🔐 Constitutional PIN: 841921")
        print(f"🎯 Active Trades: {status['active_trades']}/{status['max_concurrent']}")
        print(f"📈 Daily Trades: {status['daily_trades']}/{status['daily_limit']}")
        print(f"💱 Forex Pairs: {status['forex_pairs_monitored']} (FVG Strategy)")
        print(f"₿ Crypto Pairs: {status['crypto_pairs_monitored']} (Momentum Strategy)")
        print(f"✅ Strategies: {', '.join(status['strategies_active'])}")


def main():
    """Test the master strategy coordinator"""
    print("🚀 UNIBOT MASTER STRATEGY - TEST MODE")
    print("🔐 Constitutional PIN: 841921")
    
    try:
        master = UnibotMasterStrategy()
        master.display_status()
        
        print("\\n✅ Master Strategy Coordinator Ready")
        print("🎯 Ready to coordinate FVG + Momentum strategies")
        
    except Exception as e:
        print(f"❌ Master strategy error: {e}")


if __name__ == "__main__":
    main()
