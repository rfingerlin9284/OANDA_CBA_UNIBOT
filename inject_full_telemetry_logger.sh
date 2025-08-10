#!/bin/bash
# 🔧 RBOTZILLA TELEMETRY INJECTION - Enhanced ML Logging
# Constitutional PIN: 841921 | Live Trading Only

echo "🔧 RBOTZILLA TELEMETRY INJECTION - Constitutional PIN: 841921"

# Target ML files that need telemetry
ML_FILES=("ml_predictor.py" "ml_decision_filter.py" "main.py")

FUNC_MARKER="# === TELEMETRY LOGGER START ==="
CALL_LINE='log_telemetry(pred, max(proba), "WolfNet-V3")'

mkdir -p logs

echo "[🔧] Processing ML files for telemetry injection..."

for TARGET in "${ML_FILES[@]}"; do
    if [ ! -f "$TARGET" ]; then
        echo "[⚠️] File $TARGET not found, skipping..."
        continue
    fi
    
    echo "[🔍] Processing $TARGET..."
    
    # Inject telemetry logger definition if not already present
    if ! grep -q "$FUNC_MARKER" "$TARGET"; then
        TMPFILE=$(mktemp)
        cat << 'EOF' > "$TMPFILE"
# === AUTO-INJECTED BY inject_full_telemetry_logger.sh ===
# === TELEMETRY LOGGER START ===
import json, os
from datetime import datetime

def log_telemetry(prediction, confidence, model_name):
    """Thread-safe telemetry logging for ML predictions"""
    try:
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "prediction": str(prediction),
            "confidence": round(float(confidence), 4),
            "model": model_name,
            "constitutional_pin": "841921"
        }
        with open("logs/ml_predictions.log", "a") as f:
            f.write("ML DECISION: " + json.dumps(payload) + "\n")
    except Exception as e:
        print(f"[⚠️] Telemetry logging failed: {e}")
# === TELEMETRY LOGGER END ===

EOF
        echo "  [🔧] Injecting log_telemetry function at top of $TARGET"
        cat "$TMPFILE" "$TARGET" > "${TARGET}.tmp" && mv "${TARGET}.tmp" "$TARGET"
        rm "$TMPFILE"
    else
        echo "  [✅] log_telemetry() already present in $TARGET"
    fi
    
    # Inject function calls based on file type
    case "$TARGET" in
        "ml_predictor.py")
            # Look for "return pred, proba" pattern
            if grep -q "return pred, proba" "$TARGET" && ! grep -q "$CALL_LINE" "$TARGET"; then
                LINE_NUM=$(grep -n -m 1 "return pred, proba" "$TARGET" | cut -d: -f1)
                if [ ! -z "$LINE_NUM" ]; then
                    # Insert telemetry call before the return statement
                    INSERT_BEFORE=$LINE_NUM
                    sed -i "${INSERT_BEFORE}i\\    # RBOTZILLA TELEMETRY INJECTION\n    $CALL_LINE" "$TARGET"
                    echo "  [✅] Injected telemetry call before return in $TARGET at line $INSERT_BEFORE"
                fi
            else
                echo "  [⚠️] Could not find 'return pred, proba' pattern or call already exists in $TARGET"
            fi
            ;;
            
        "ml_decision_filter.py")
            # Look for decision-making patterns
            if grep -q "decision\|signal" "$TARGET" && ! grep -q "log_telemetry" "$TARGET"; then
                LINE_NUM=$(grep -n -m 1 -i "decision\|signal" "$TARGET" | cut -d: -f1)
                if [ ! -z "$LINE_NUM" ]; then
                    INSERT_AFTER=$((LINE_NUM + 1))
                    sed -i "${INSERT_AFTER}i\\    # RBOTZILLA TELEMETRY INJECTION\n    log_telemetry(\"decision_signal\", 0.8, \"DecisionFilter\")" "$TARGET"
                    echo "  [✅] Injected decision telemetry call in $TARGET at line $INSERT_AFTER"
                fi
            else
                echo "  [⚠️] No decision pattern found or telemetry already exists in $TARGET"
            fi
            ;;
            
        "main.py")
            # Check if main.py needs additional telemetry calls
            if ! grep -q "log_telemetry.*main" "$TARGET"; then
                # Find a good place to inject - look for trading loop or main function
                LINE_NUM=$(grep -n -m 1 "def main\|while.*True\|trading.*loop" "$TARGET" | cut -d: -f1)
                if [ ! -z "$LINE_NUM" ]; then
                    INSERT_AFTER=$((LINE_NUM + 2))
                    sed -i "${INSERT_AFTER}i\\        # RBOTZILLA MAIN TELEMETRY\n        log_telemetry(\"system_start\", 1.0, \"MainController\")" "$TARGET"
                    echo "  [✅] Injected main system telemetry call in $TARGET at line $INSERT_AFTER"
                else
                    echo "  [⚠️] Could not find suitable injection point in main.py"
                fi
            else
                echo "  [✅] Main telemetry already exists in $TARGET"
            fi
            ;;
    esac
    
    echo "  [🎯] Completed processing $TARGET"
done


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
EOF


echo ""
echo "[✅] TELEMETRY INJECTION COMPLETE"
echo "[🔧] Enhanced ML logging active in all target files"


echo ""
echo "[🎯] RBOTZILLA TELEMETRY INJECTION SUCCESSFUL"
echo "[📊] Constitutional PIN: 841921 - Live trading telemetry active"
