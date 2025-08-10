#!/usr/bin/env python3
"""
🛠️ Retrain Heavy Model with Final 8 Features
Rebuilds ../models/light_heavy_model.pkl with exact feature alignment for hybrid engine
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
import os

def generate_synthetic_training_data():
    """Generate synthetic training data with exact 8 features"""
    print("🔄 Generating synthetic training data with 8-feature alignment...")
    
    # Generate 10,000 synthetic samples
    np.random.seed(42)
    n_samples = 10000
    
    data = {
        'rsi': np.random.uniform(20, 80, n_samples),
        'ema_cross': np.random.choice([0, 1], n_samples),
        'fvg_strength': np.random.uniform(0, 1, n_samples),
        'volume_ratio': np.random.uniform(0.5, 2.0, n_samples),
        'oanda_order_imbalance': np.random.uniform(-0.5, 0.5, n_samples),
        'coinbase_order_imbalance': np.random.uniform(-0.5, 0.5, n_samples),
        'session_bias': np.random.choice([0, 1, 2], n_samples),  # US, EU, ASIA
        'volatility': np.random.uniform(0.1, 0.8, n_samples)
    }
    
    # Create realistic labels based on feature combinations
    labels = []
    for i in range(n_samples):
        # Simple logic: bullish if RSI < 30 and EMA cross positive and FVG strong
        score = 0
        if data['rsi'][i] < 30:
            score += 1
        if data['ema_cross'][i] == 1:
            score += 1
        if data['fvg_strength'][i] > 0.7:
            score += 1
        if data['volume_ratio'][i] > 1.5:
            score += 1
        if data['oanda_order_imbalance'][i] > 0.2:
            score += 1
        
        # 1 = bullish, 0 = bearish
        labels.append(1 if score >= 3 else 0)
    
    data['label'] = labels
    df = pd.DataFrame(data)
    return df

def retrain_heavy_model():
    """Retrain the heavy model with correct 8-feature alignment"""
    print("🧠 Starting Heavy Model Retraining Process...")
    
    # Generate or load training data
        print("📂 Loading existing labeled data...")
    else:
        print("📊 Generating synthetic training data...")
        df = generate_synthetic_training_data()
    
    # ✅ Final 8 feature columns (EXACT match with hybrid engine)
    features = [
        'rsi', 'ema_cross', 'fvg_strength', 'volume_ratio',
        'oanda_order_imbalance', 'coinbase_order_imbalance',
        'session_bias', 'volatility'
    ]
    
    # Ensure all features exist
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        print(f"⚠️  Missing features: {missing_features}")
        print("🔧 Adding missing features with default values...")
        for feature in missing_features:
            if feature in ['ema_cross', 'session_bias']:
                df[feature] = np.random.choice([0, 1], len(df))
            else:
                df[feature] = np.random.uniform(0, 1, len(df))
    
    X = df[features]
    y = df['label'] if 'label' in df.columns else np.random.choice([0, 1], len(df))
    
    print(f"📊 Training data shape: {X.shape}")
    print(f"📊 Feature columns: {list(X.columns)}")
    
    # Split data
    
    # 🧠 Train Random Forest with optimized parameters
    print("🤖 Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=7,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Test accuracy
    train_score = model.score(X_train, y_train)
    print(f"📈 Training accuracy: {train_score:.3f}")
    
    # Feature importance
    feature_importance = dict(zip(features, model.feature_importances_))
    print("🎯 Feature Importance:")
    for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
        print(f"   {feature}: {importance:.3f}")
    
    # 💾 Save to model path
    model_path = 'models/../models/light_heavy_model.pkl'
    joblib.dump(model, model_path)
    print(f"[✅] Heavy model retrained and saved to: {model_path}")
    
    # Verify the saved model
    loaded_model = joblib.load(model_path)
    print(f"🔍 Verification: Loaded model expects {loaded_model.n_features_in_} features")
    
    return model

if __name__ == "__main__":
    retrain_heavy_model()
    print("\n🎉 Heavy model retraining complete! Model is now aligned with hybrid engine.")
