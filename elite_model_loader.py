#!/usr/bin/env python3
"""
🏆 ELITE MODEL LOADER - 18+18 Dual Architecture
Constitutional PIN: 841921
"""
import json
import pickle
import os

class EliteModelManager:
    def __init__(self, config_path="live_config_elite.json"):
        self.constitutional_pin = "841921"
        self.load_config(config_path)
        self.forex_model = None
        self.crypto_model = None
        self.load_models()
    
    def load_config(self, config_path):
        """Load elite 18+18 configuration"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            self.config = config['elite_trading_config']
            self.forex_pairs = self.config['trading_pairs']['forex']
            self.crypto_pairs = self.config['trading_pairs']['crypto']
            
            print(f"✅ Elite Config Loaded: {len(self.forex_pairs)} FX + {len(self.crypto_pairs)} Crypto")
            
        except Exception as e:
            print(f"⚠️ Config load failed: {e}")
            # Fallback to hardcoded elite pairs
            self.forex_pairs = [
                "EUR_USD", "USD_JPY", "GBP_USD", "USD_CHF", "AUD_USD", "NZD_USD",
                "EUR_JPY", "GBP_JPY", "EUR_GBP", "USD_CAD", "EUR_CHF", "AUD_JPY", 
                "CHF_JPY", "GBP_CHF", "NZD_JPY", "CAD_JPY", "EUR_AUD", "GBP_AUD"
            ]
            self.crypto_pairs = [
                "BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD", "XRP-USD", "ADA-USD",
                "AVAX-USD", "LINK-USD", "MATIC-USD", "DOT-USD", "LTC-USD", "APT-USD",
                "BCH-USD", "UNI-USD", "OP-USD", "NEAR-USD", "INJ-USD", "XLM-USD"
            ]
    
    def load_models(self):
        """Load both elite models"""
        try:
            # Load Forex model
            with open("models/forex_elite_18.pkl", "rb") as f:
                self.forex_model = pickle.load(f)
            print("✅ Forex Elite Model: LOADED")
        except Exception as e:
            print(f"⚠️ Forex model load failed: {e}")
            
        try:
            # Load Crypto model  
            with open("models/crypto_elite_18.pkl", "rb") as f:
                self.crypto_model = pickle.load(f)
            print("✅ Crypto Elite Model: LOADED")
        except Exception as e:
            print(f"⚠️ Crypto model load failed: {e}")
    
    def get_model_for_pair(self, pair):
        """Return appropriate model for trading pair"""
        if any(forex_pair in pair for forex_pair in ["EUR", "USD", "GBP", "JPY", "CHF", "AUD", "NZD", "CAD"]):
            return self.forex_model, "forex"
        else:
            return self.crypto_model, "crypto"
    
    def get_all_pairs(self):
        """Return all 36 pairs"""
        return {
            'forex': self.forex_pairs,
            'crypto': self.crypto_pairs,
            'total': len(self.forex_pairs) + len(self.crypto_pairs)
        }
    
    def system_status(self):
        """Elite system status"""
        forex_status = "✅ LOADED" if self.forex_model else "⚠️ FALLBACK"
        crypto_status = "✅ LOADED" if self.crypto_model else "⚠️ FALLBACK"
        
        print(f"🏆 ELITE 18+18 SYSTEM STATUS")
        print(f"📈 Forex Model ({len(self.forex_pairs)} pairs): {forex_status}")
        print(f"💰 Crypto Model ({len(self.crypto_pairs)} pairs): {crypto_status}")
        print(f"🎯 Total Coverage: {len(self.forex_pairs) + len(self.crypto_pairs)} pairs")
        print(f"🔐 Constitutional PIN: {self.constitutional_pin}")

if __name__ == "__main__":
    manager = EliteModelManager()
    manager.system_status()
