#!/bin/bash
# RBOTzilla Megalithic Groom + Launch Script
# ✅ Validates every file
# ✅ Flags and logs mismatches
# ✅ Generates restoration + rebuild templates
# ✅ Auto-launches swarm after verification
# Run this with: bash groom_and_launch.sh

BASE="/home/ing/overlord/wolfpack-lite/oanda_cba_unibot"
MANUAL_MD="$BASE/RBOTzilla_Developer_Quality_Manual.md"
FLAG_LOG="$BASE/logs/groom_flags.log"
RESTORATION_SCRIPT="$BASE/restoration.sh"
TEMPLATE_REBUILD="$BASE/template_rebuild.sh"
MAIN_EXEC="$BASE/main.py"

# 🧹 Prep logs and outputs
mkdir -p "$BASE/logs"
echo "==== RBOTzilla Groom Started: $(date) ====" > "$FLAG_LOG"
echo "#!/bin/bash" > "$RESTORATION_SCRIPT"
echo "# Auto-Generated Restoration Script" >> "$RESTORATION_SCRIPT"
chmod +x "$RESTORATION_SCRIPT"

# 🔍 Groom Function
groom_tree() {
  echo "🔍 Scanning file tree..."
  find "$BASE" -type f -not -path "$BASE/logs/*" -not -name "*.log" | while read -r file; do
    rel_path="${file#$BASE/}"
    if grep -q "$rel_path" "$MANUAL_MD"; then
      echo "✅ $rel_path matches manual" | tee -a "$FLAG_LOG"
    else
      echo "❌ $rel_path NOT FOUND in manual – POSSIBLE CODE MISSING" | tee -a "$FLAG_LOG"
      echo "# Restore $rel_path" >> "$RESTORATION_SCRIPT"
      echo "echo \"Restoring $rel_path\"" >> "$RESTORATION_SCRIPT"
      echo "cat << 'EOF' > \"$file\"" >> "$RESTORATION_SCRIPT"
      cat "$file" >> "$RESTORATION_SCRIPT"
      echo "EOF" >> "$RESTORATION_SCRIPT"
    fi
  done
}

# 🧱 Rebuild Skeleton
build_template_skeleton() {
  echo "🔧 Generating blank rebuild template..."
  echo "#!/bin/bash" > "$TEMPLATE_REBUILD"
  echo "# Blank Template Rebuild - RBOTzilla" >> "$TEMPLATE_REBUILD"
  echo "mkdir -p $BASE/{config,models,logs,strategies,core,utils}" >> "$TEMPLATE_REBUILD"
  echo "touch $BASE/{main.py,launch_live_swarm.sh,live_battle_narrator.py,requirements.txt,start.sh}" >> "$TEMPLATE_REBUILD"
  echo "touch $BASE/logs/{live_trades.log,ml_predictions.log}" >> "$TEMPLATE_REBUILD"
  echo "echo \"Blank bot structure rebuilt. Populate with code from manual.\"" >> "$TEMPLATE_REBUILD"
  chmod +x "$TEMPLATE_REBUILD"
}

# 🧠 Final Deploy Check
launch_swarm_if_ready() {
  echo "🚦 Verifying integrity before launch..."
  if grep -q "❌" "$FLAG_LOG"; then
    echo "⚠️ Mismatches found in file tree. Review $FLAG_LOG before live launch."
    echo "To restore: bash $RESTORATION_SCRIPT"
    exit 1
  else
    echo "🟢 All systems GO. Launching live swarm..."
    python3 "$MAIN_EXEC"
  fi
}

# 🚀 Launch Sequence
groom_tree
build_template_skeleton
launch_swarm_if_ready
