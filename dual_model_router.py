#!/usr/bin/env python3
"""
🧠 AI Model Routing System - RBOTzilla Elite 18+18
Constitutional PIN: 841921
"""
import pickle
import logging

class DualModelRouter:
    def __init__(self):
        self.constitutional_pin = "841921"
        self.forex_model = None
        self.crypto_model = None
        self.load_models()
        
    def load_models(self):
        """Load both forex and crypto models"""
        try:
                self.forex_model = pickle.load(f)
            print("✅ Forex Model: Loaded")
            
                self.crypto_model = pickle.load(f)
            print("✅ Crypto Model: Loaded")
            
        except Exception as e:
            print(f"⚠️ Model loading error: {e}")
            
    def route_prediction(self, instrument, features):
        """Route prediction to appropriate model"""
        if any(currency in instrument for currency in ["EUR", "USD", "GBP", "JPY"]):
            model = self.forex_model
            model_type = "FOREX"
        else:
            model = self.crypto_model  
            model_type = "CRYPTO"
            
        if model:
            try:
                prediction = model.predict([features])[0]
                confidence = max(model.predict_proba([features])[0])
                
                logging.info(f"{model_type} PREDICTION: {instrument} -> {prediction} (conf: {confidence:.3f})")
                return prediction, confidence
            except:
                return 0, 0.5
        else:
            return 0, 0.5

if __name__ == "__main__":
    router = DualModelRouter()
    print("🧠 Dual Model Router: Ready for predictions")
