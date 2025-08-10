#!/bin/bash
TARGET="/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/autonomous_startup.py"

sed -i '/LIVE_TRADING_ENABLED/d' "$TARGET"
sed -i '/SANDBOX_BACKTEST_MODE/d' "$TARGET"
sed -i '1iLIVE_TRADING_ENABLED = False' "$TARGET"
sed -i '2iSANDBOX_BACKTEST_MODE = True' "$TARGET"

