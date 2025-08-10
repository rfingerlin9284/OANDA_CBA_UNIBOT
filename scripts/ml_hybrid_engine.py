import joblib
import os
import numpy as np

HEAVY_MODEL_PATH = "./models/../models/light_heavy_model.pkl"

class HybridMLEngine:
    def __init__(self):
        self.light_model = None
        self.heavy_model = None
        self._load_models()

    def _load_models(self):
        try:
            self.light_model = joblib.load(LIGHT_MODEL_PATH)
            self.heavy_model = joblib.load(HEAVY_MODEL_PATH)
            print("[✅] Models loaded into hybrid engine.")
        except Exception as e:
            print(f"[❌] Failed to load ML models: {e}")

    def predict_light(self, features: dict):
        try:
            x = np.array([[features[k] for k in ['rsi', 'ema_cross', 'fvg_strength', 'volume_ratio']]])
            return float(self.light_model.predict_proba(x)[0][1])
        except Exception as e:
            print(f"[❌] Light prediction failed: {e}")
            return 0.0

    def predict_heavy(self, features: dict):
        try:
            x = np.array([[features[k] for k in [
                'rsi', 'ema_cross', 'fvg_strength', 'volume_ratio',
                'oanda_order_imbalance', 'coinbase_order_imbalance',
                'session_bias', 'volatility'
            ]]])
            return float(self.heavy_model.predict_proba(x)[0][1])
        except Exception as e:
            print(f"[❌] Heavy prediction failed: {e}")
            return 0.0
