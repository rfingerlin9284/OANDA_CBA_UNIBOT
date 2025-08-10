#!/usr/bin/env python3
"""
🧪 RBOTZILLA TELEMETRY TEST
Constitutional PIN: 841921
"""
import sys
sys.path.append('.')

    print("🧪 RBOTZILLA TELEMETRY TEST - Constitutional PIN: 841921")
    
    try:
        # Test ml_predictor telemetry
        from ml_predictor import run_prediction, load_model
        print("[✅] ml_predictor imports successful")
        
        # Run a mock prediction to generate telemetry
        model = load_model("nonexistent.pkl")  # This will use fallback
        features = {"price": 1.0, "volume": 100}
        pred, proba = run_prediction(model, features)
        print(f"[🔍] Mock prediction: {pred}, confidence: {max(proba)}")
        
        # Check if telemetry log was created
        import os
        if os.path.exists("logs/ml_predictions.log"):
            with open("logs/ml_predictions.log", "r") as f:
                lines = f.readlines()
                recent_lines = lines[-3:]  # Get last 3 lines
                print(f"[✅] Telemetry log found with {len(lines)} entries")
                for i, line in enumerate(recent_lines):
                    print(f"   {i+1}: {line.strip()}")
        else:
            print("[⚠️] Telemetry log not found")
        
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
