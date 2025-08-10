#!/bin/bash
# === ONE-SHOT FVG STRATEGY REPAIR (NO TA-LIB, NO INDENT ERRORS) ===

cd ~/overlord/wolfpack-lite/oanda_cba_unibot

TARGET="fvg_strategy.py"

echo "🚩 Checking for empty main guards..."
# Remove any 'if __name__ == "__main__":' with nothing below it (blank or just pass)
awk '
  /^\s*if __name__ == .__main__.:\s*$/ {
    getline nextline
    if (nextline ~ /^[[:space:]]*$/ || nextline ~ /^[[:space:]]*pass[[:space:]]*$/) next
  }
  {print}
' $TARGET > ${TARGET}.fixed && mv ${TARGET}.fixed $TARGET

echo "🚩 Checking for misplaced FVGStrategy instantiations..."
# Move any 'strategy = FVGStrategy()' lines OUT of class indentation (should not be inside class)
sed -i '/class FVGStrategy:/,/^class /{s/^[[:space:]]*strategy = FVGStrategy()/strategy = FVGStrategy()/}' $TARGET
# Also nuke if accidentally inside class
sed -i '/class FVGStrategy:/,/^class /{/strategy = FVGStrategy()/d}' $TARGET
# Ensure only at file-level, not in class

# If the last line is 'strategy = FVGStrategy()', keep it there (safe), else append
if ! grep -q "^strategy = FVGStrategy()" $TARGET; then
  echo -e "\nstrategy = FVGStrategy()" >> $TARGET
fi

echo "🛠️  Reformatting indentation (spaces only)..."
# Replace tabs with 4 spaces everywhere (paranoid)
expand -t 4 $TARGET > tmp && mv tmp $TARGET

echo "🧹 Final syntax check..."
python3 -c "from fvg_strategy import FVGStrategy; print('✅ FVGStrategy import successful!')" 2>&1 | tee /tmp/fvg_test.log

if grep -q "IndentationError" /tmp/fvg_test.log; then
    echo "❌ Indentation still broken. See /tmp/fvg_test.log for details."
    tail -n 10 /tmp/fvg_test.log
else
    echo "✅ fvg_strategy.py is fixed and ready. Fire away!"
fi
