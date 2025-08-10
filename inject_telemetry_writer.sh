#!/bin/bash
TARGET="core_logic.py"  # 🔁 Change this to your real model file name
TELEMETRY_FUNC_DEF=$(
cat <<EOF
def log_telemetry(prediction, confidence_score, model_name):
    import json, time
    payload = {
        "timestamp": time.time(),
        "model": model_name,
        "prediction": str(prediction),
        "confidence": round(float(confidence_score), 4)
    }
    with open("logs/ml_predictions.log", "a") as f:
        f.write(json.dumps(payload) + "\\n")
EOF
)

echo "📌 Scanning $TARGET..."

if ! grep -q "def log_telemetry" "$TARGET"; then
    echo "🧠 Inserting log_telemetry() function at top of $TARGET..."
    TMPFILE=$(mktemp)
    echo "$TELEMETRY_FUNC_DEF" > "$TMPFILE"
    echo "" >> "$TMPFILE"
    cat "$TARGET" >> "$TMPFILE"
    mv "$TMPFILE" "$TARGET"
else
    echo "✅ log_telemetry() already defined. Skipping definition insert."
fi

echo "🔍 Finding insertion point..."
LINE_NUM=$(grep -n -m 1 "prediction =" "$TARGET" | cut -d: -f1)
if [ -z "$LINE_NUM" ]; then
    echo "❌ Cannot find 'prediction =' line. Aborting injection."
    exit 1
fi

INSERT_AFTER=$((LINE_NUM + 1))
echo "🪛 Inserting log_telemetry(...) after line $LINE_NUM..."
sed -i "${INSERT_AFTER}i\\
    log_telemetry(prediction, confidence_score, model_name)" "$TARGET"

echo "✅ Injection complete in $TARGET"
#!/bin/bash
TARGET="core_logic.py"  # 🔁 Change this to your real model file name
TELEMETRY_FUNC_DEF=$(
cat <<EOF
def log_telemetry(prediction, confidence_score, model_name):
    import json, time
    payload = {
        "timestamp": time.time(),
        "model": model_name,
        "prediction": str(prediction),
        "confidence": round(float(confidence_score), 4)
    }
    with open("logs/ml_predictions.log", "a") as f:
        f.write(json.dumps(payload) + "\\n")
EOF
)

echo "📌 Scanning $TARGET..."

if ! grep -q "def log_telemetry" "$TARGET"; then
    echo "🧠 Inserting log_telemetry() function at top of $TARGET..."
    TMPFILE=$(mktemp)
    echo "$TELEMETRY_FUNC_DEF" > "$TMPFILE"
    echo "" >> "$TMPFILE"
    cat "$TARGET" >> "$TMPFILE"
    mv "$TMPFILE" "$TARGET"
else
    echo "✅ log_telemetry() already defined. Skipping definition insert."
fi

echo "🔍 Finding insertion point..."
LINE_NUM=$(grep -n -m 1 "prediction =" "$TARGET" | cut -d: -f1)
if [ -z "$LINE_NUM" ]; then
    echo "❌ Cannot find 'prediction =' line. Aborting injection."
    exit 1
fi

INSERT_AFTER=$((LINE_NUM + 1))
echo "🪛 Inserting log_telemetry(...) after line $LINE_NUM..."
sed -i "${INSERT_AFTER}i\\
    log_telemetry(prediction, confidence_score, model_name)" "$TARGET"

echo "✅ Injection complete in $TARGET"
