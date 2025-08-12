#!/usr/bin/env python3
"""
🔥 ENHANCED FUTURES TRADING ENGINE
Integrates Coinbase futures with HIVE MIND RICK system
Combines price action, sentiment analysis, and risk management
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Add parent directory for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class FuturesSignalGenerator:
    """Generate trading signals for futures contracts using multiple indicators"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.futures_dir = self.data_dir / "futures"
        self.sentiment_dir = self.data_dir / "cryptopanic"
        
        # Trading parameters
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        self.volatility_threshold = 5.0
        self.confidence_threshold = 0.65
        
        print("🔥 FUTURES SIGNAL GENERATOR INITIALIZED")
    
    def load_futures_data(self, contract: str) -> Optional[pd.DataFrame]:
        """Load futures data from CSV"""
        filename = f"{contract.replace('-', '_')}_crypto_futures.csv"
        filepath = self.futures_dir / filename
        
        if not filepath.exists():
            print(f"⚠️ No data found for {contract}")
            return None
        
        try:
            df = pd.read_csv(filepath)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"❌ Error loading {contract} data: {e}")
            return None
    
    def load_latest_sentiment(self) -> Optional[Dict]:
        """Load latest sentiment analysis"""
        try:
            sentiment_files = list(self.sentiment_dir.glob("sentiment_*.json"))
            if not sentiment_files:
                print("⚠️ No sentiment data found")
                return None
            
            # Get most recent sentiment file
            latest_file = max(sentiment_files, key=lambda x: x.stat().st_mtime)
            
            with open(latest_file, 'r') as f:
                sentiment_data = json.load(f)
            
            return sentiment_data['sentiment_analysis']
        except Exception as e:
            print(f"❌ Error loading sentiment: {e}")
            return None
    
    def calculate_technical_signals(self, df: pd.DataFrame) -> Dict:
        """Calculate technical analysis signals"""
        if len(df) < 20:
            return {'signal': 'HOLD', 'confidence': 0.0, 'reason': 'Insufficient data'}
        
        latest = df.iloc[-1]
        signals = []
        
        # RSI signals
        if latest['RSI'] < self.rsi_oversold:
            signals.append(('BUY', 0.3, 'RSI Oversold'))
        elif latest['RSI'] > self.rsi_overbought:
            signals.append(('SELL', 0.3, 'RSI Overbought'))
        
        # Moving average signals
        if latest['close'] > latest['SMA_20'] > latest['SMA_50']:
            signals.append(('BUY', 0.25, 'Bullish MA'))
        elif latest['close'] < latest['SMA_20'] < latest['SMA_50']:
            signals.append(('SELL', 0.25, 'Bearish MA'))
        
        # Volatility signals
        if latest['volatility'] > self.volatility_threshold:
            signals.append(('HOLD', 0.2, 'High volatility'))
        
        # Price momentum
        price_change = (latest['close'] - df.iloc[-5]['close']) / df.iloc[-5]['close'] * 100
        if price_change > 2:
            signals.append(('BUY', 0.2, 'Strong momentum'))
        elif price_change < -2:
            signals.append(('SELL', 0.2, 'Weak momentum'))
        
        # Aggregate signals
        buy_weight = sum(weight for signal, weight, _ in signals if signal == 'BUY')
        sell_weight = sum(weight for signal, weight, _ in signals if signal == 'SELL')
        
        if buy_weight > sell_weight and buy_weight > 0.5:
            final_signal = 'BUY'
            confidence = min(buy_weight, 1.0)
        elif sell_weight > buy_weight and sell_weight > 0.5:
            final_signal = 'SELL'
            confidence = min(sell_weight, 1.0)
        else:
            final_signal = 'HOLD'
            confidence = 0.3
        
        return {
            'signal': final_signal,
            'confidence': confidence,
            'reasons': [reason for _, _, reason in signals],
            'rsi': latest['RSI'],
            'price': latest['close'],
            'volatility': latest['volatility']
        }
    
    def apply_sentiment_filter(self, technical_signal: Dict, sentiment: Dict) -> Dict:
        """Apply sentiment analysis to technical signals"""
        if sentiment is None:
            return technical_signal
        
        sentiment_score = sentiment['overall']
        sentiment_strength = abs(sentiment_score)
        
        # Modify confidence based on sentiment alignment
        if technical_signal['signal'] == 'BUY' and sentiment_score > 0:
            # Bullish sentiment supports buy signal
            technical_signal['confidence'] += sentiment_strength * 0.2
            technical_signal['reasons'].append(f"Positive sentiment ({sentiment_score:.2f})")
        elif technical_signal['signal'] == 'SELL' and sentiment_score < 0:
            # Bearish sentiment supports sell signal
            technical_signal['confidence'] += sentiment_strength * 0.2
            technical_signal['reasons'].append(f"Negative sentiment ({sentiment_score:.2f})")
        elif sentiment_strength > 0.5:
            # Strong opposing sentiment - reduce confidence
            technical_signal['confidence'] *= (1 - sentiment_strength * 0.3)
            technical_signal['reasons'].append(f"Conflicting sentiment ({sentiment_score:.2f})")
        
        # Cap confidence at 1.0
        technical_signal['confidence'] = min(technical_signal['confidence'], 1.0)
        
        return technical_signal
    
    def calculate_position_size(self, signal: Dict, account_balance: float, risk_per_trade: float = 0.02) -> float:
        """Calculate position size based on signal confidence and risk management"""
        base_risk = account_balance * risk_per_trade
        confidence_multiplier = signal['confidence']
        
        # Reduce size for high volatility
        volatility_factor = max(0.5, 1 - (signal['volatility'] / 20))
        
        position_size = base_risk * confidence_multiplier * volatility_factor
        return round(position_size, 2)
    
    def generate_signals_for_all_contracts(self) -> Dict:
        """Generate signals for all futures contracts"""
        print("\n🎯 GENERATING FUTURES TRADING SIGNALS")
        print("=" * 50)
        
        contracts = [
            "BTC-USD", "ETH-USD", "XRP-USD", "SOL-USD",
            "DOGE-USD", "LINK-USD", "LTC-USD", "MATIC-USD"
        ]
        
        # Load sentiment once
        sentiment = self.load_latest_sentiment()
        if sentiment:
            print(f"📰 Sentiment loaded: Overall {sentiment['overall']:.2f}")
        
        signals = {}
        
        for contract in contracts:
            print(f"\n🔍 Analyzing {contract}...")
            
            # Load data
            df = self.load_futures_data(contract)
            if df is None:
                continue
            
            # Generate technical signals
            tech_signal = self.calculate_technical_signals(df)
            
            # Apply sentiment filter
            final_signal = self.apply_sentiment_filter(tech_signal, sentiment)
            
            # Calculate position size (assuming $10,000 account)
            position_size = self.calculate_position_size(final_signal, 10000)
            
            signals[contract] = {
                **final_signal,
                'position_size': position_size,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Print signal summary
            if final_signal['confidence'] >= self.confidence_threshold:
                action = final_signal['signal']
                conf = final_signal['confidence']
                size = position_size
                print(f"   🎯 {action} signal - Confidence: {conf:.2f} - Size: ${size}")
            else:
                print(f"   ⏸️  HOLD - Low confidence ({final_signal['confidence']:.2f})")
        
        return signals
    
    def save_signals(self, signals: Dict):
        """Save generated signals to JSON file"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"futures_signals_{timestamp}.json"
        filepath = self.data_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(signals, f, indent=2, default=str)
        
        print(f"\n💾 Signals saved to {filepath}")
        return filepath

def main():
    """Main execution function"""
    print("🔥 HIVE MIND RICK - FUTURES SIGNAL GENERATOR")
    print("=" * 60)
    
    generator = FuturesSignalGenerator()
    
    try:
        # Generate signals
        signals = generator.generate_signals_for_all_contracts()
        
        # Save signals
        filepath = generator.save_signals(signals)
        
        # Summary
        strong_signals = [k for k, v in signals.items() if v['confidence'] >= 0.65]
        total_contracts = len(signals)
        
        print(f"\n🎉 SIGNAL GENERATION COMPLETE!")
        print(f"📊 Total contracts analyzed: {total_contracts}")
        print(f"🎯 Strong signals generated: {len(strong_signals)}")
        print(f"💾 Signals saved to: {filepath}")
        
        if strong_signals:
            print(f"\n🚀 STRONG SIGNALS:")
            for contract in strong_signals:
                signal = signals[contract]
                print(f"   {contract}: {signal['signal']} ({signal['confidence']:.2f}) - ${signal['position_size']}")
        
    except Exception as e:
        print(f"❌ Signal generation failed: {e}")
        raise

if __name__ == "__main__":
    main()
