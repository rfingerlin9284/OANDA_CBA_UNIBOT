#!/bin/bash
# 🔀 RBOTZILLA MODE TOGGLE
# Constitutional PIN: 841921

echo "🔀 RBOTZILLA MODE TOGGLE"
echo "1) 🔴 LIVE MODE (Real Money)"
echo "2) 🟡 SANDBOX MODE (Paper Trading)"
echo ""
read -p "Select mode (1 or 2): " MODE

case $MODE in
    1)
        echo "🔐 CONSTITUTIONAL PIN VERIFICATION FOR LIVE MODE"
        read -s -p "Enter Constitutional PIN: " PIN
        echo ""
        if [ "$PIN" != "841921" ]; then
            echo "❌ INVALID PIN - ACCESS DENIED"
            exit 1
        fi
        echo "✅ LAUNCHING LIVE MODE"
        python3 main.py --live --secure --constitutional-pin 841921 --narration
        ;;
    2)
        echo "✅ LAUNCHING SANDBOX MODE"
        ;;
    *)
        echo "❌ Invalid selection"
        exit 1
        ;;
esac
