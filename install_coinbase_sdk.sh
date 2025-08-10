#!/bin/bash
# install_coinbase_sdk.sh: Install official SDK
cd /home/ing/overlord/wolfpack-lite/oanda_cba_unibot
source venv/bin/activate
pip install coinbase-advanced-py
echo "[✅] coinbase-advanced-py installed for ED25519 auth."
