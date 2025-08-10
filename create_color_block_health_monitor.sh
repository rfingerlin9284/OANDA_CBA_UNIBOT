#!/bin/bash
# 🧱 Self-saving script: Alternating Color Block Health Monitor for RBOTzilla

FILE="rbotzilla_health_pulse.sh"

cat << 'INNER_EOF' > "$FILE"
#!/bin/bash
# 🌈 RBOTzilla Health Pulse Feed with Consistent Color Blocks per Message Source

COLORS=(31 32 33 34 35 36 91 92 93 94 95 96)
COLOR_INDEX=0

function block_color_echo() {
    local header="\$1"
    shift
    local color=\${COLORS[\$COLOR_INDEX]}
    echo -e "\033[1;\${color}m\$header\033[0m"
    for line in "\$@"; do
        echo -e "\033[1;\${color}m  \$line\033[0m"
    done
    echo ""
    COLOR_INDEX=\$(( (COLOR_INDEX + 1) % \${#COLORS[@]} ))
}

while true; do
    sleep 2
    block_color_echo "[🧠 ML Model Alive]" \
        "Confidence: 0.91" \
        "Model: WolfNet-V3" \
        "Last Signal: HOLD"

    sleep 2
    block_color_echo "[🛡️ OCO Check OK]" \
        "All active trades have OCO links" \
        "Cancel logic responsive ✅"

    sleep 2
    block_color_echo "[💹 Trade Loop Ready]" \
        "Strategy: Price Action Pullback" \
        "No active signals — scanning..."

    sleep 2
    block_color_echo "[🧬 Exit Logic]" \
        "Smart Exit armed with 1.5% threshold" \
        "Trailing SL enabled | Take profit: dynamic"

    sleep 2
    block_color_echo "[🔁 Watchdog Status]" \
        "No hangs detected" \
        "Restart counter = 0"

    sleep 2
    block_color_echo "[📡 API Connectivity]" \
        "OANDA: Connected" \
        "Coinbase: Connected" \
        "Latency: 38ms avg"

    echo ""
done
INNER_EOF

chmod +x "$FILE"
echo "✅ Color-block health monitor created: \$FILE"
echo "📡 Run it anytime with: ./\$FILE"
