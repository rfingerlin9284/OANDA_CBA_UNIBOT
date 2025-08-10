#!/usr/bin/env python3
"""
🔥 Quick Heavy Model Creation
Creates a matching heavy model with 8 features for immediate deployment
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import pickle
import os

def create_heavy_model():
    """Create heavy model with same feature structure as light model"""
    print("[🔥] Creating Heavy Model...")
    
    # Generate synthetic training data matching light model
    np.random.seed(123)  # Different seed for diversity
    n_samples = 15000    # More samples for heavy model
    
    # Generate features identical to light model
    data = {
        'rsi': np.random.normal(50, 15, n_samples),
        'ema_cross': np.random.choice([0, 1], n_samples),
        'fvg_strength': np.random.uniform(0, 1, n_samples),
        'volume_ratio': np.random.lognormal(0, 0.5, n_samples),
        'oanda_order_imbalance': np.random.normal(0, 0.1, n_samples),
        'coinbase_order_imbalance': np.random.normal(0, 0.1, n_samples),
        'session_bias': np.random.choice([0, 1, 2], n_samples),
        'volatility': np.random.exponential(0.02, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create more sophisticated target for heavy model
    df['target'] = (
        (df['rsi'] < 25) |  # Stronger oversold
        (df['rsi'] > 75) |  # Stronger overbought
        (df['ema_cross'] == 1) & (df['fvg_strength'] > 0.5) |  # Combined signals
        (df['fvg_strength'] > 0.8) |  # Very strong FVG
        (abs(df['oanda_order_imbalance']) > 0.03) & (abs(df['coinbase_order_imbalance']) > 0.03) |  # Both orderbooks
        (df['session_bias'] == 1) & (df['volatility'] < 0.01)  # London session with low volatility
    ).astype(int)
    
    # Prepare features (exact same order as light model)
    feature_cols = ['rsi', 'ema_cross', 'fvg_strength', 'volume_ratio', 
                   'oanda_order_imbalance', 'coinbase_order_imbalance', 
                   'session_bias', 'volatility']
    
    X = df[feature_cols]
    y = df['target']
    
    # Train heavy model (more complex)
    model = GradientBoostingClassifier(
        n_estimators=200,   # More trees
        max_depth=15,       # Deeper trees
        learning_rate=0.05, # Slower learning
        random_state=123,
        subsample=0.8
    )
    
    model.fit(X, y)
    
    # Evaluate
    train_score = model.score(X, y)
    print(f"[📊] Heavy Model - Train Score: {train_score:.3f}")
    
    # Save model
    os.makedirs("models", exist_ok=True)
        pickle.dump(model, f)
    
    print(f"[🔧] Model expects {len(feature_cols)} features: {feature_cols}")
    
    return model

if __name__ == "__main__":
    create_heavy_model()
