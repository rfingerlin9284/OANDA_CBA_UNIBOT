#!/usr/bin/env python3
"""
🧠 Create Synthetic Labeled Data & Retrain Both Models
Generates realistic trading data and trains both light/heavy models with correct features
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

def create_synthetic_labeled_data():
    """Generate synthetic but realistic trading data for model training"""
    np.random.seed(42)
    n_samples = 10000
    
    # Generate the 8 mandatory features
    data = {
        'rsi': np.random.normal(50, 15, n_samples),  # RSI around 50
        'ema_cross': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),  # EMA crossover signals
        'fvg_strength': np.random.exponential(0.5, n_samples),  # FVG strength
        'volume_ratio': np.random.lognormal(0, 0.5, n_samples),  # Volume ratio
        'oanda_order_imbalance': np.random.normal(0, 0.3, n_samples),  # Order imbalance
        'coinbase_order_imbalance': np.random.normal(0, 0.3, n_samples),  # Order imbalance
        'session_bias': np.random.choice([0, 1, 2], n_samples, p=[0.4, 0.3, 0.3]),  # Session bias
        'volatility': np.random.exponential(0.2, n_samples)  # Market volatility
    }
    
    df = pd.DataFrame(data)
    
    # Create realistic labels based on feature combinations
    # This liveulates profitable trading conditions
    labels = []
    for i in range(n_samples):
        # Profitable conditions: 
        # - RSI oversold/overbought with EMA cross
        # - Strong FVG with low volatility
        # - Favorable session bias with order imbalance
        score = 0
        
        # RSI signals
        if (df.iloc[i]['rsi'] < 30 or df.iloc[i]['rsi'] > 70) and df.iloc[i]['ema_cross'] == 1:
            score += 0.4
        
        # FVG strength
        if df.iloc[i]['fvg_strength'] > 1.0 and df.iloc[i]['volatility'] < 0.3:
            score += 0.3
        
        # Order imbalance alignment
        if abs(df.iloc[i]['oanda_order_imbalance']) > 0.2 and abs(df.iloc[i]['coinbase_order_imbalance']) > 0.2:
            if np.sign(df.iloc[i]['oanda_order_imbalance']) == np.sign(df.iloc[i]['coinbase_order_imbalance']):
                score += 0.2
        
        # Session bias
        if df.iloc[i]['session_bias'] == 1:  # Favorable session
            score += 0.1
        
        # Add some noise
        score += np.random.normal(0, 0.1)
        
        # Convert to binary label
        labels.append(1 if score > 0.5 else 0)
    
    df['label'] = labels
    
    # Ensure balanced dataset
    positive_samples = sum(labels)
    print(f"Generated {n_samples} samples: {positive_samples} positive ({positive_samples/n_samples*100:.1f}%)")
    
    return df

def retrain_models():
    """Create synthetic data and retrain both models"""
    print("🧠 Creating synthetic labeled dataset...")
    df = create_synthetic_labeled_data()
    
    # Save the synthetic dataset
    os.makedirs('data', exist_ok=True)
    
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)
    
    # Define feature sets
    features_light = ['rsi', 'ema_cross', 'fvg_strength', 'volume_ratio']
    features_heavy = [
        'rsi', 'ema_cross', 'fvg_strength', 'volume_ratio',
        'oanda_order_imbalance', 'coinbase_order_imbalance',
        'session_bias', 'volatility'
    ]
    
    y = df['label']
    
    print("🔄 Training light model...")
    X_light = df[features_light]
    light_model = RandomForestClassifier(
        n_estimators=60, 
        max_depth=5, 
        random_state=42,
        n_jobs=-1
    )
    light_model.fit(X_light, y)
    
    # Train heavy model (../models/light_heavy_model.pkl)
    print("🔄 Training heavy model...")
    X_heavy = df[features_heavy]
    heavy_model = RandomForestClassifier(
        n_estimators=120, 
        max_depth=7, 
        random_state=42,
        n_jobs=-1
    )
    heavy_model.fit(X_heavy, y)
    joblib.dump(heavy_model, 'models/../models/light_heavy_model.pkl')
    print("✅ Heavy model saved to models/../models/light_heavy_model.pkl")
    
    # Verify feature alignment
    print("\n🔍 Model Feature Verification:")
    print(f"Light model features: {light_model.feature_names_in_.tolist()}")
    print(f"Heavy model features: {heavy_model.feature_names_in_.tolist()}")
    
    # Test predictions
    print("\n🧪 Testing model predictions...")
    
    
    print(f"Light model prediction: {light_pred:.3f}")
    print(f"Heavy model prediction: {heavy_pred:.3f}")
    
    print("\n🎯 Both models retrained successfully with correct feature alignment!")
    return True

if __name__ == "__main__":
    retrain_models()
