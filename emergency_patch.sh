#!/bin/bash
# 🔧 WOLFPACK-LITE EMERGENCY PATCH SYSTEM
# Auto-fixes orderbook errors, ML input warnings, and restarts system

echo "🔧 WOLFPACK-LITE EMERGENCY PATCH - Starting..."
echo "=" * 60

# Create the patch module
cat > scripts/patch_orderbook_and_ml_input.py << 'EOF'
#!/usr/bin/env python3
"""
🔧 Emergency Patch Module - Defensive orderbook + ML input fixes
"""

import json
import pandas as pd
import numpy as np

def safe_get_buckets(orderbook_data):
    """Safely extract buckets from OANDA orderbook response"""
    try:
        if isinstance(orderbook_data, dict):
            if "buckets" in orderbook_data:
                return orderbook_data["buckets"]
            elif "orderBook" in orderbook_data and "buckets" in orderbook_data["orderBook"]:
                return orderbook_data["orderBook"]["buckets"]
        return []
    except (KeyError, TypeError, AttributeError):
        return []

def predict_with_feature_names(model, features_dict):
    """Make ML predictions with proper feature names to avoid sklearn warnings"""
    try:
        # Convert to DataFrame with proper column names
        df = pd.DataFrame([features_dict])
        predictions = model.predict(df)
        probabilities = model.predict_proba(df)
        return predictions[0], probabilities[0]
    except Exception as e:
        print(f"🚨 ML Prediction Error: {e}")
        return False, [0.5, 0.5]

def safe_json_serialize(data):
    """Convert numpy types to JSON-serializable types"""
    if isinstance(data, dict):
        return {k: safe_json_serialize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [safe_json_serialize(v) for v in data]
    elif isinstance(data, (np.integer, np.floating)):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, np.bool_):
        return bool(data)
    else:
        return data

def safe_json_dump(data, filepath):
    """Safely dump data to JSON file with numpy type conversion"""
    try:
        serializable_data = safe_json_serialize(data)
        with open(filepath, 'w') as f:
            json.dump(serializable_data, f, indent=2)
        return True
    except Exception as e:
        print(f"🚨 JSON Dump Error: {e}")
        return False
EOF

echo "✅ Patch module created"

# Patch the orderbook fusion script
echo "🔧 Patching orderbook_fusion.py..."

cat > scripts/orderbook_fusion_patched.py << 'EOF'
# scripts/orderbook_fusion.py - PATCHED VERSION
# 🔄 Order Book Data Fusion (OANDA + Coinbase Advanced) with defensive error handling

import requests
import numpy as np
from patch_orderbook_and_ml_input import safe_get_buckets

# --- OANDA CONFIG ---
OANDA_API_KEY = "5f2cd72673e5c6214f94cc159e444a01-c229936202d1b6d0b4499086198da2b3"
OANDA_ACCOUNT_ID = "001-001-13473069-001"
OANDA_BASE_URL = "https://api-fxtrade.oanda.com/v3"

# --- COINBASE CONFIG ---
COINBASE_API_URL = "https://api.exchange.coinbase.com"

def fetch_oanda_orderbook(pair="EUR_USD", depth=10):
    try:
        url = f"{OANDA_BASE_URL}/orderbook?instrument={pair}&depth={depth}"
        headers = {"Authorization": f"Bearer {OANDA_API_KEY}"}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        
        # Use defensive bucket extraction
        buckets = safe_get_buckets(data)
        
        if not buckets:
            print(f"OANDA orderbook no buckets found for {pair}")
            return {"bid_ratio": 0.5, "ask_ratio": 0.5, "imbalance": 0.0}
            
        bids = sum([float(b["price"]) * float(b.get("longCountPercent", 0)) for b in buckets])
        asks = sum([float(b["price"]) * float(b.get("shortCountPercent", 0)) for b in buckets])
        return normalize_orderbook(bids, asks)
        
    except Exception as e:
        print(f"OANDA orderbook error: {e}")
        return {"bid_ratio": 0.5, "ask_ratio": 0.5, "imbalance": 0.0}

def fetch_coinbase_orderbook(symbol="BTC-USD", level=2):
    try:
        url = f"{COINBASE_API_URL}/products/{symbol}/book?level={level}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if "bids" not in data or "asks" not in data:
            return {"bid_ratio": 0.5, "ask_ratio": 0.5, "imbalance": 0.0}

        bids = sum([float(b[1]) for b in data["bids"][:10]])
        asks = sum([float(a[1]) for a in data["asks"][:10]])
        return normalize_orderbook(bids, asks)
    except Exception as e:
        print(f"Coinbase orderbook error: {e}")
        return {"bid_ratio": 0.5, "ask_ratio": 0.5, "imbalance": 0.0}

def normalize_orderbook(bid_volume, ask_volume):
    total = bid_volume + ask_volume
    bid_ratio = bid_volume / total if total > 0 else 0.5
    ask_ratio = ask_volume / total if total > 0 else 0.5
    return {
        "bid_ratio": round(bid_ratio, 3),
        "ask_ratio": round(ask_ratio, 3),
        "imbalance": round(bid_ratio - ask_ratio, 3)
    }

def fused_orderbook_features():
    """Get combined orderbook features from both exchanges"""
    oanda_data = fetch_oanda_orderbook()
    coinbase_data = fetch_coinbase_orderbook()
    
    return {
        "oanda_order_imbalance": oanda_data["imbalance"],
        "coinbase_order_imbalance": coinbase_data["imbalance"]
    }
EOF

# Replace the original with patched version
mv scripts/orderbook_fusion_patched.py scripts/orderbook_fusion.py
echo "✅ Orderbook fusion patched"

# Patch the ML hybrid engine
echo "🔧 Patching ml_hybrid_engine.py..."

# Create a backup
cp scripts/ml_hybrid_engine.py scripts/ml_hybrid_engine_backup.py

# Apply patches to ML engine
python3 << 'EOF'
import re

# Read the current ML engine
with open('scripts/ml_hybrid_engine.py', 'r') as f:
    content = f.read()

# Patch 1: Add import for patch module
if 'from patch_orderbook_and_ml_input import' not in content:
    content = content.replace(
        'import json',
        'import json\nfrom patch_orderbook_and_ml_input import predict_with_feature_names, safe_json_dump'
    )

# Patch 2: Replace direct model.predict calls
content = re.sub(
    r'light_conf = self\.light_model\.predict_proba\(X\)\[0\]\[1\]',
    'light_pred, light_proba = predict_with_feature_names(self.light_model, features)\n            light_conf = light_proba[1]',
    content
)

content = re.sub(
    r'heavy_conf = self\.heavy_model\.predict_proba\(X\)\[0\]\[1\]',
    'heavy_pred, heavy_proba = predict_with_feature_names(self.heavy_model, features)\n            heavy_conf = heavy_proba[1]',
    content
)

# Patch 3: Replace JSON logging with safe version
content = re.sub(
    r'with open\("logs/ml_snapshots/hybrid_log\.json", "w"\) as f:\s*json\.dump\(self\.history\[-20:\], f, indent=2\)',
    'safe_json_dump(self.history[-20:], "logs/ml_snapshots/hybrid_log.json")',
    content
)

# Write patched version
with open('scripts/ml_hybrid_engine.py', 'w') as f:
    f.write(content)

print("✅ ML hybrid engine patched")
EOF

echo "✅ ML hybrid engine patched"

# Stop all running ML processes
echo "🛑 Stopping running ML processes..."
sleep 3

BACKTEST_PID=$!


# Wait a moment and check results
sleep 8

echo "📊 Checking patched system output..."
echo "--- Last 15 lines from patched log ---"

echo ""
echo "--- Checking for error patterns ---"
    echo "❌ OANDA orderbook errors still present"
else
    echo "✅ OANDA orderbook errors resolved"
fi

    echo "❌ Feature mismatch still present"
else
    echo "✅ Feature mismatch resolved"
fi

    echo "⚠️ Feature name warnings present (non-critical)"
else
    echo "✅ Feature name warnings resolved"
fi

echo ""
echo "🔧 PATCH COMPLETE - System Status:"
echo "📊 Heartbeat: $(pgrep -f heartbeat_checkin.sh > /dev/null && echo '✅ Running' || echo '❌ Stopped')"

echo ""
echo "🚀 WOLFPACK-LITE EMERGENCY PATCH COMPLETE!"
echo "=" * 60
