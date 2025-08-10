#!/bin/bash
echo "🔥 MASTER RBOTZILLA COINBASE ED25519 JWT AUTH PROTOCOL"
echo "=" * 60

cd /home/ing/overlord/wolfpack-lite/oanda_cba_unibot
source venv/bin/activate

echo "Step 1: Installing dependencies..."
bash fix_coinbase_dep.sh

echo -e "\nStep 2: Generating ED25519 key pair..."
bash generate_ed25519_key.sh

echo -e "\nStep 3: Generating JWT token..."
bash generate_jwt.sh

echo -e "\nStep 4: Testing authentication..."

echo -e "\nStep 5: Creating fixed API handler..."
bash fix_coinbase_api.sh

echo -e "\nStep 6: Testing fixed API..."
python3 coinbase_advanced_api_fixed.py

echo -e "\n🎯 PRE-DEPLOYMENT TEST COMPLETE!"
echo "Check logs above for any errors."
echo -e "\nNext steps:"
echo "- Say 'go headless' to launch swarm in live mode"
echo "- Say 'inject dashboard' for visual overlay"
echo "- Constitutional PIN: 841921"
