#!/bin/bash
# fix_coinbase_dep.sh: Install cryptography for ED25519
cd /home/ing/overlord/wolfpack-lite/oanda_cba_unibot
source venv/bin/activate
pip install cryptography PyJWT --no-cache-dir
echo "[✅] Cryptography and PyJWT installed for ED25519 support."
