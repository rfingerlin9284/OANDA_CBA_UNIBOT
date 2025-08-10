#!/usr/bin/env python3
"""
🛠️ Retrain Main Wolfpack ML Model with 8-Feature Alignment
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
import os

def retrain_main_model():
    """Retrain the main wolfpack ML model with correct 8-feature alignment"""
    print("🧠 Starting Main Wolfpack Model Retraining...")
    
    # Load the same training data
        print("📂 Loading existing labeled data...")
    else:
        print("❌ No training data found. Please run retrain_heavy_model.py first.")
        return
    
    # ✅ Final 8 feature columns (EXACT match with hybrid engine)
    features = [
        'rsi', 'ema_cross', 'fvg_strength', 'volume_ratio',
        'oanda_order_imbalance', 'coinbase_order_imbalance',
        'session_bias', 'volatility'
    ]
    
    X = df[features]
    y = df['label']
    
    print(f"📊 Training data shape: {X.shape}")
    print(f"📊 Feature columns: {list(X.columns)}")
    
    # Split data
    
    # 🧠 Train Random Forest with slightly different parameters for main model
    print("🤖 Training Main Wolfpack ML model...")
    model = RandomForestClassifier(
        n_estimators=150,  # More trees for main model
        max_depth=8,       # Slightly deeper
        min_samples_split=8,
        min_samples_leaf=4,
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
    joblib.dump(model, model_path)
    print(f"[✅] Main Wolfpack model retrained and saved to: {model_path}")
    
    # Verify the saved model
    loaded_model = joblib.load(model_path)
    print(f"🔍 Verification: Loaded model expects {loaded_model.n_features_in_} features")
    
    return model

if __name__ == "__main__":
    retrain_main_model()
    print("\n🎉 Main Wolfpack ML model retraining complete! Both models now aligned.")
