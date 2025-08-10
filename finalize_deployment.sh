#!/bin/bash
# 🔐 RBOTzilla Final Live System Merge (Excludes models)

SRC="/home/ing/overlord/wolfpack-lite/oanda_cba_unibot_live"
DEST="/home/ing/overlord/wolfpack-lite/oanda_cba_unibot"
LEGACY="/home/ing/overlord/wolfpack-lite/DONT USE LEGACY ONLY"
LOG="deployment_sync_excluding_models.log"

echo "🧼 Preparing final deployment..."
sleep 1

# Step 1: Ensure folders exist
if [ ! -d "$SRC" ]; then
  echo "❌ Legacy folder not found: $SRC"
  exit 1
fi

mkdir -p "$DEST"

# Step 2: Rsync everything EXCEPT 'models/'
echo "📦 Syncing from legacy to active (excluding models)..."
rsync -av --progress \
  --exclude 'models/' \
  "$SRC/" "$DEST/" >> "$LOG"

# Step 3: Copy top-level files individually if needed
for f in main.py launch_live_swarm.sh live_battle_narrator.py requirements.txt start.sh
do
  if [ -f "$SRC/$f" ]; then
    cp "$SRC/$f" "$DEST/"
    echo "✅ Copied $f"
  fi
done

# Step 4: Rename legacy folder
echo "📛 Renaming legacy folder to: DONT USE LEGACY ONLY"
mv "$SRC" "$LEGACY"

# Step 5: Lock down destination folder
echo "🔐 Making $DEST immutable with chattr..."
sudo chattr -R +i "$DEST"

# Step 6: Confirm results
echo ""
echo "📂 Final structure (LEVEL 2):"
tree -L 2 "$DEST"

echo ""
echo "✅ LIVE SYSTEM FINALIZED — MODELS UNTOUCHED"
echo "🧱 ACTIVE BOT: $DEST"
echo "🚫 LEGACY FOLDER: $LEGACY"
echo "📜 LOG FILE: $LOG"
