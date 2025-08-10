#!/usr/bin/env python3
"""
🧠 HEAVY MODEL TRAINER - OANDA/Coinbase Hybrid
Trains heavyweight ML model for deep strategy filtering
"""

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
from datetime import datetime

def prepare_advanced_training_data():
    """Prepare advanced training data with more sophisticated features"""
    features = []
    labels = []
    
    print("📊 Loading historical data for heavy model...")
    
    # Process Coinbase data with advanced features
    coinbase_dir = "data/coinbase/"
    if os.path.exists(coinbase_dir):
        for file in os.listdir(coinbase_dir):
            if file.endswith('.csv'):
                try:
                    df = pd.read_csv(os.path.join(coinbase_dir, file))
                    if len(df) > 200:  # More data needed for complex model
                        pair_features, pair_labels = extract_advanced_features_from_df(df, file)
                        features.extend(pair_features)
                        labels.extend(pair_labels)
                        print(f"  ✅ Processed {file}: {len(pair_features)} samples")
                except Exception as e:
                    print(f"  ⚠️ Error processing {file}: {e}")
    
    # Process OANDA data with advanced features
    oanda_dir = "data/oanda/"
    if os.path.exists(oanda_dir):
        for file in os.listdir(oanda_dir):
            if file.endswith('.csv'):
                try:
                    df = pd.read_csv(os.path.join(oanda_dir, file))
                    if len(df) > 200:  # More data needed for complex model
                        pair_features, pair_labels = extract_advanced_features_from_df(df, file)
                        features.extend(pair_features)
                        labels.extend(pair_labels)
                        print(f"  ✅ Processed {file}: {len(pair_features)} samples")
                except Exception as e:
                    print(f"  ⚠️ Error processing {file}: {e}")
    
    if not features:
        print("❌ No training data found!")
        return None, None
    
    return np.array(features), np.array(labels)

def extract_advanced_features_from_df(df, filename):
    """Extract advanced trading features from OHLCV data"""
    features = []
    labels = []
    
    # Ensure required columns exist
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required_cols):
        return [], []
    
    # Calculate advanced technical indicators
    df['rsi'] = calculate_rsi(df['close'])
    df['ema_12'] = df['close'].ewm(span=12).mean()
    df['ema_26'] = df['close'].ewm(span=26).mean()
    df['macd'] = df['ema_12'] - df['ema_26']
    df['bb_upper'], df['bb_lower'] = calculate_bollinger_bands(df['close'])
    df['atr'] = calculate_atr(df['high'], df['low'], df['close'])
    df['volume_ma'] = df['volume'].rolling(window=20).mean()
    df['price_momentum'] = df['close'].rolling(window=10).apply(lambda x: (x[-1] - x[0]) / x[0])
    df['volatility_20'] = df['close'].rolling(window=20).std()
    df['volatility_50'] = df['close'].rolling(window=50).std()
    
    # Generate advanced features and labels
    for i in range(100, len(df) - 10):  # More lookback for complex patterns
        try:
            # Advanced feature set
            feature_row = [
                df['rsi'].iloc[i] if not pd.isna(df['rsi'].iloc[i]) else 50,
                df['macd'].iloc[i] if not pd.isna(df['macd'].iloc[i]) else 0,
                (df['close'].iloc[i] - df['bb_lower'].iloc[i]) / (df['bb_upper'].iloc[i] - df['bb_lower'].iloc[i]) if not pd.isna(df['bb_upper'].iloc[i]) else 0.5,
                df['atr'].iloc[i] if not pd.isna(df['atr'].iloc[i]) else 0,
                df['volume'].iloc[i] / df['volume_ma'].iloc[i] if not pd.isna(df['volume_ma'].iloc[i]) and df['volume_ma'].iloc[i] > 0 else 1,
                df['price_momentum'].iloc[i] if not pd.isna(df['price_momentum'].iloc[i]) else 0,
                df['volatility_20'].iloc[i] / df['volatility_50'].iloc[i] if not pd.isna(df['volatility_50'].iloc[i]) and df['volatility_50'].iloc[i] > 0 else 1,
                # Pattern recognition features
                detect_hammer_pattern(df, i),
                detect_engulfing_pattern(df, i),
                detect_gap_pattern(df, i)
            ]
            
            # More sophisticated labeling (multi-period profit target)
            future_high = df['high'].iloc[i+1:i+11].max()  # Next 10 periods
            current_price = df['close'].iloc[i]
            max_profit_pct = (future_high - current_price) / current_price
            
            # Binary label: 1 if significant profit opportunity (>0.5%), 0 otherwise
            label = 1 if max_profit_pct > 0.005 else 0
            
            features.append(feature_row)
            labels.append(label)
            
        except Exception as e:
            continue
    
    return features, labels

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    except:
        return pd.Series([50] * len(prices))

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    try:
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        return upper, lower
    except:
        return pd.Series([0] * len(prices)), pd.Series([0] * len(prices))

def calculate_atr(high, low, close, period=14):
    """Calculate Average True Range"""
    try:
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()
    except:
        return pd.Series([0] * len(high))

def detect_hammer_pattern(df, i):
    """Detect hammer candlestick pattern"""
    try:
        if i < 1:
            return 0
        
        o, h, l, c = df['open'].iloc[i], df['high'].iloc[i], df['low'].iloc[i], df['close'].iloc[i]
        body = abs(c - o)
        lower_shadow = min(o, c) - l
        upper_shadow = h - max(o, c)
        
        # Hammer pattern conditions
        if body > 0 and lower_shadow > 2 * body and upper_shadow < body * 0.5:
            return 1
        return 0
    except:
        return 0

def detect_engulfing_pattern(df, i):
    """Detect engulfing candlestick pattern"""
    try:
        if i < 1:
            return 0
        
        # Current candle
        o1, c1 = df['open'].iloc[i], df['close'].iloc[i]
        # Previous candle
        o0, c0 = df['open'].iloc[i-1], df['close'].iloc[i-1]
        
        # Bullish engulfing
        if c0 < o0 and c1 > o1 and o1 < c0 and c1 > o0:
            return 1
        # Bearish engulfing
        elif c0 > o0 and c1 < o1 and o1 > c0 and c1 < o0:
            return -1
        return 0
    except:
        return 0

def detect_gap_pattern(df, i):
    """Detect gap patterns (FVG-like)"""
    try:
        if i < 2:
            return 0
        
        h0 = df['high'].iloc[i-2]
        l1 = df['low'].iloc[i]
        gap = l1 - h0
        
        # Significant gap detection
        avg_range = (df['high'].iloc[i-10:i] - df['low'].iloc[i-10:i]).mean()
        if gap > avg_range * 0.5:
            return 1
        elif gap < -avg_range * 0.5:
            return -1
        return 0
    except:
        return 0

def train_heavy_model():
    """Train the heavyweight ML model"""
    print("🚀 Starting Heavy Model Training...")
    
    # Prepare advanced data
    X, y = prepare_advanced_training_data()
    if X is None or len(X) == 0:
        print("❌ No training data available")
        return False
    
    print(f"📊 Training data: {len(X)} samples, {len(X[0])} features")
    
    # Split data
    
    # Train heavy model (more complex - deeper analysis)
    model = GradientBoostingClassifier(
        n_estimators=200,  # More trees for deeper learning
        max_depth=8,
        learning_rate=0.1,
        random_state=42
    )
    
    print("🧠 Training heavy model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    
    feature_names = ['RSI', 'MACD', 'BB_Position', 'ATR', 'Volume_Ratio', 'Momentum', 'Vol_Ratio', 'Hammer', 'Engulfing', 'Gap']
    print(f"✅ Model Accuracy: {accuracy:.3f}")
    print(f"📈 Feature Importance: {dict(zip(feature_names, model.feature_importances_))}")
    
    # Save model
    os.makedirs("models", exist_ok=True)
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"💾 Heavy model saved to {model_path}")
    
    # Log training info
    training_log = {
        'timestamp': datetime.now().isoformat(),
        'model_type': 'heavy_model',
        'accuracy': accuracy,
        'samples': len(X),
        'features': len(X[0]),
        'model_path': model_path
    }
    
    os.makedirs("logs/ml_snapshots", exist_ok=True)
    with open("logs/ml_snapshots/heavy_training_log.json", "w") as f:
        import json
        json.dump(training_log, f, indent=2)
    
    return True

if __name__ == "__main__":
    success = train_heavy_model()
    if success:
        print("🎯 Heavy model training completed successfully!")
    else:
        print("❌ Heavy model training failed!")
