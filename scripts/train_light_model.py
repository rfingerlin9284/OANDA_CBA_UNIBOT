#!/usr/bin/env python3
"""
🏋️ Light Model Trainer - Fast Decision Engine
Trains lightweight ML model for quick trade decisions
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
from datetime import datetime, timedelta

def generate_training_data():
    """Generate synthetic training data based on trading patterns"""
    np.random.seed(42)
    n_samples = 10000
    
    # Generate features liveilar to your trading system
    data = {
        'rsi': np.random.normal(50, 15, n_samples),
        'ema_cross': np.random.choice([0, 1], n_samples),
        'fvg_strength': np.random.uniform(0, 1, n_samples),
        'volume_ratio': np.random.lognormal(0, 0.5, n_samples),
        'oanda_order_imbalance': np.random.normal(0, 0.1, n_samples),
        'coinbase_order_imbalance': np.random.normal(0, 0.1, n_samples),
        'session_bias': np.random.choice([0, 1, 2], n_samples),  # Asian, London, NY
        'volatility': np.random.exponential(0.02, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create target based on realistic trading logic
    df['target'] = (
        (df['rsi'] < 30) |  # Oversold
        (df['rsi'] > 70) |  # Overbought
        (df['ema_cross'] == 1) |  # EMA crossover
        (df['fvg_strength'] > 0.7) |  # Strong FVG
        (abs(df['oanda_order_imbalance']) > 0.05)  # Strong orderbook imbalance
    ).astype(int)
    
    return df

def train_light_model():
    """Train the light model for fast decisions"""
    print("[🏋️] Training Light Model...")
    
    # Generate or load training data
    df = generate_training_data()
    
    # Prepare features and target
    feature_cols = ['rsi', 'ema_cross', 'fvg_strength', 'volume_ratio', 
                   'oanda_order_imbalance', 'coinbase_order_imbalance', 
                   'session_bias', 'volatility']
    
    X = df[feature_cols]
    y = df['target']
    
    # Split data
    
    # Train light model (fast but less complex)
    model = RandomForestClassifier(
        n_estimators=50,  # Fewer trees for speed
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    
    
    # Save model
    os.makedirs("models", exist_ok=True)
    with open("models/../models/light_heavy_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print("[✅] Light Model saved to models/../models/light_heavy_model.pkl")
    
    return model

if __name__ == "__main__":
    train_light_model()
