#!/bin/bash
# 🔁 Patch persistent ML execution loop into main.py

TARGET="main.py"
LOOP_MARKER="RBOTzilla Swarm Bot is live"

echo "📌 Injecting persistent execution loop into $TARGET..."

# Backup original
cp "$TARGET" "${TARGET}.bak"
echo "🛡️ Backup saved as ${TARGET}.bak"

# Check if already patched
if grep -q "$LOOP_MARKER" "$TARGET"; then
    echo "⚠️ Loop already present — skipping injection."
    exit 0
fi

# Append main loop block
cat << 'EOF' >> "$TARGET"

if __name__ == "__main__":
    print("🚀 RBOTzilla Swarm Bot is live. Beginning operations...")
    while True:
        try:
            system_check()
            for pair in config.get("pairs", []):
                prediction, confidence_score = predict_trade(model, pair)
                model_name = "WolfNet-V3"
                log_telemetry(prediction, confidence_score, model_name)
                # TODO: Add trade execution logic here if needed
                time.sleep(3)
        except Exception as e:
            print(f"⚠️ Exception occurred: {e}")
            time.sleep(5)
EOF

echo "✅ Main loop injected into $TARGET"
