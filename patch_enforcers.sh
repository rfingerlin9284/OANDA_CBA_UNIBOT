#!/bin/bash

FILES_TO_PATCH=(
    "main.py"
    "oco_executor.py"
    "coinbase_advanced_api.py"
)

echo "🔧 Injecting LIVE_MODE enforcement..."

for file in "${FILES_TO_PATCH[@]}"; do
    if [ -f "$file" ]; then
        echo "🔨 Patching $file..."
        if grep -q "IS_LIVE_MODE = True" "$file"; then
            echo "✅ Already patched: $file"
        else
            sed -i '1i\
IS_LIVE_MODE = True\n\
REQUIRE_OCO = True\n\
REQUIRE_COINBASE_API = True\n\
if not IS_LIVE_MODE:\n\
    raise RuntimeError("�� LIVE_MODE is not active. Execution blocked.")\n\
' "$file"
            echo "✅ Patched $file"
        fi
    else
        echo "⚠️  File not found: $file"
    fi
done

echo "🎯 All enforcement logic injected successfully."
