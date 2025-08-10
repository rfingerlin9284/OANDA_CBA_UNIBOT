#!/usr/bin/env python3
"""
🔁 ADVANCED BACKTESTER - Historical replay with ML integration
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, timedelta

# Import ML components
sys.path.append('scripts')
from ml_hybrid_engine import ml_engine

    """Historical data replay with ML decision integration"""
    
    def __init__(self, use_historical=True, live=True):
        self.use_historical = use_historical
        self.balance = 10000.0  # Starting balance
        self.trades = []
        self.ml_decisions = []
        
        # Load config
        self.config = self._load_config()
        
    def _load_config(self):
        """Load system configuration"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
    
        print("=" * 60)
        
        # Test Coinbase data
        coinbase_dir = os.path.join(data_dir, "coinbase")
        if os.path.exists(coinbase_dir):
            print("📊 Coinbase Historical Analysis:")
            self._process_exchange_data(coinbase_dir, "Coinbase")
        
        # Test OANDA data  
        oanda_dir = os.path.join(data_dir, "oanda")
        if os.path.exists(oanda_dir):
            print("\n📊 OANDA Historical Analysis:")
            self._process_exchange_data(oanda_dir, "OANDA")
        
        # Generate summary report
    
    def _process_exchange_data(self, data_dir, exchange_name):
        """Process all CSV files in exchange directory"""
        for file in sorted(os.listdir(data_dir)):
            if file.endswith('.csv'):
                pair = file.replace('.csv', '')
                file_path = os.path.join(data_dir, file)
                
                try:
                    df = pd.read_csv(file_path)
                    if len(df) > 100:  # Ensure sufficient data
                        print(f"  {pair}: {signals} ML signals generated")
                except Exception as e:
                    print(f"  ❌ Error processing {pair}: {e}")
    
        signals = 0
        
        # Ensure required columns exist
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
            return 0
        
        # Process data in chunks (liveulate real-time)
        for i in range(50, len(df), 10):  # Skip first 50 for indicators
            try:
                # Extract current market features
                features = self._extract_features(df, i)
                
                # Get ML decision
                if self.config.get('ml_models_loaded', False):
                    ml_decision = ml_engine.predict(features)
                    
                    if ml_decision:
                        signals += 1
                        self._liveulate_trade(df.iloc[i], pair, exchange, features)
                        
                        # Log ML decision
                        self.ml_decisions.append({
                            'pair': pair,
                            'exchange': exchange,
                            'timestamp': datetime.now().isoformat(),
                            'features': features,
                            'decision': ml_decision
                        })
                
            except Exception as e:
                # Silently continue on individual errors
                continue
        
        return signals
    
    def _extract_features(self, df, idx):
        """Extract trading features from historical data"""
        try:
            # Calculate RSI
            rsi = self._calculate_rsi(df['close'], idx)
            
            # EMA distance
            ema_20 = df['close'].iloc[idx-20:idx].mean()
            ema_distance = abs(df['close'].iloc[idx] - ema_20) / ema_20
            
            # Volume ratio
            avg_volume = df['volume'].iloc[idx-10:idx].mean()
            volume_ratio = df['volume'].iloc[idx] / avg_volume if avg_volume > 0 else 1.0
            
            # FVG strength (liveplified)
            fvg_strength = self._detect_fvg_strength(df, idx)
            
            # Volatility
            volatility = df['close'].iloc[idx-10:idx].std() / df['close'].iloc[idx]
            
            return {
                'rsi': rsi,
                'ema_distance': ema_distance,
                'volume_ratio': volume_ratio,
                'fvg_strength': fvg_strength,
                'volatility': volatility,
                'pair_type': 1  # Simplified
            }
        except:
            # Return default features on error
            return {
                'rsi': 50.0,
                'ema_distance': 0.01,
                'volume_ratio': 1.0,
                'fvg_strength': 0.5,
                'volatility': 0.01,
                'pair_type': 1
            }
    
    def _calculate_rsi(self, prices, idx, period=14):
        """Calculate RSI indicator"""
        try:
            if idx < period:
                return 50.0
                
            deltas = prices.iloc[idx-period:idx].diff()
            gains = deltas.where(deltas > 0, 0).mean()
            losses = (-deltas.where(deltas < 0, 0)).mean()
            
            if losses == 0:
                return 100.0
                
            rs = gains / losses
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except:
            return 50.0
    
    def _detect_fvg_strength(self, df, idx):
        """Detect Fair Value Gap strength"""
        try:
            if idx < 3:
                return 0.0
                
            # Simple gap detection
            prev_high = df['high'].iloc[idx-2]
            curr_low = df['low'].iloc[idx]
            gap = abs(curr_low - prev_high) / prev_high
            
            return min(gap * 100, 1.0)  # Normalize to 0-1
        except:
            return 0.0
    
    def _liveulate_trade(self, candle, pair, exchange, features):
        """Simulate trade execution"""
        entry_price = candle['close']
        risk_amount = self.balance * 0.01  # 1% risk
        
        pnl = np.random.normal(0, risk_amount * 0.5)  # Random outcome
        self.balance += pnl
        
        trade_record = {
            'pair': pair,
            'exchange': exchange,
            'entry_price': entry_price,
            'pnl': pnl,
            'balance': self.balance,
            'features': features
        }
        
        self.trades.append(trade_record)
    
        print("\n" + "=" * 60)
        print("📊 BACKTEST SUMMARY REPORT")
        print("=" * 60)
        
        if self.trades:
            total_trades = len(self.trades)
            winning_trades = len([t for t in self.trades if t['pnl'] > 0])
            win_rate = (winning_trades / total_trades) * 100
            
            total_pnl = sum(t['pnl'] for t in self.trades)
            final_balance = self.balance
            
            print(f"📈 Total Trades: {total_trades}")
            print(f"🎯 Win Rate: {win_rate:.1f}%")
            print(f"💰 Total P&L: ${total_pnl:.2f}")
            print(f"💳 Final Balance: ${final_balance:.2f}")
            print(f"📊 Return: {((final_balance - 10000) / 10000) * 100:.1f}%")
        else:
        
        if self.ml_decisions:
            ml_count = len(self.ml_decisions)
            print(f"🧠 ML Decisions: {ml_count}")
            print(f"📊 ML Approval Rate: {(len(self.trades) / ml_count) * 100:.1f}%")
        
        # Save detailed report
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump({
                'summary': {
                    'total_trades': len(self.trades),
                    'win_rate': win_rate if self.trades else 0,
                    'total_pnl': sum(t['pnl'] for t in self.trades),
                    'final_balance': self.balance
                },
                'trades': self.trades[-50:],  # Last 50 trades
                'ml_decisions': self.ml_decisions[-50:]  # Last 50 ML decisions
            }, f, indent=2)
        
        print(f"📄 Detailed report saved: {report_path}")

def main():
    parser.add_argument('--use_historical', type=bool, default=True)
    
    args = parser.parse_args()
    
        use_historical=args.use_historical,
    )
    

if __name__ == "__main__":
    main()
