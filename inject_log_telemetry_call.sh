#!/bin/bash
# 🔧 Auto-inject telemetry call into model loop

TARGET="core_logic.py"  # ✅ Update if your file has a different name
CALL_LINE='log_telemetry(prediction, confidence_score, model_name)'

echo "📌 Checking if $CALL_LINE already exists..."
if grep -q "$CALL_LINE" "$TARGET"; then
    echo "⚠️  log_telemetry call already present. Skipping injection."
    exit 0
fi

echo "🧠 Locating insertion point in $TARGET..."
LINE_NUM=$(grep -n -m 1 "prediction =" "$TARGET" | cut -d: -f1)

if [ -z "$LINE_NUM" ]; then
    echo "❌ Couldn't find a suitable insertion point in $TARGET."
    exit 1
fi

echo "🪛 Inserting telemetry logger call after line $LINE_NUM..."
INSERT_AFTER=$((LINE_NUM + 1))

# Inject cleanly using sed
sed -i "${INSERT_AFTER}i\\
    $CALL_LINE" "$TARGET"

echo "✅ Injected: $CALL_LINE into $TARGET at line $INSERT_AFTER"
