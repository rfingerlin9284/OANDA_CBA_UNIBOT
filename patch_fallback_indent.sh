#!/bin/bash
# 🧼 Patch bad indentation in main.py (line 44 fallback function)

TARGET="main.py"
PATCH_START_LINE=44
FUNC_NAME="get_trading_stats_fallback"

echo "📌 Patching fallback function in $TARGET..."

# Create temp file with clean fallback function
cat << 'EOF' > /tmp/fallback_patch.tmp
def get_trading_stats_fallback():
    return {
        "prediction": "N/A",
        "confidence": 0.0,
        "model": "N/A",
        "timestamp": datetime.utcnow().isoformat()
    }
EOF

# Backup original
cp "$TARGET" "${TARGET}.bak"
echo "🛡️ Backup saved as ${TARGET}.bak"

# Remove broken block from line 44 downward (until next blank or def/class)
awk -v start="$PATCH_START_LINE" -v func="$FUNC_NAME" '
    NR < start { print; next }
    NR == start {
        print "# [PATCHED] Replacing broken " func "() block"
        skip=1
        next
    }
    skip && /^[[:space:]]*$/ { skip=0; next }
    skip && /^[[:space:]]*(def|class)[[:space:]]/ { skip=0 }
    !skip { print }
' "$TARGET" > "${TARGET}.tmp"

# Inject patched fallback
head -n $((PATCH_START_LINE - 1)) "${TARGET}.tmp" > "${TARGET}"
cat /tmp/fallback_patch.tmp >> "${TARGET}"
tail -n +$((PATCH_START_LINE)) "${TARGET}.tmp" >> "${TARGET}"

rm -f "${TARGET}.tmp" /tmp/fallback_patch.tmp

echo "✅ Patched $FUNC_NAME() at line $PATCH_START_LINE in $TARGET"
