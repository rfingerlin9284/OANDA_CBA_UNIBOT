#!/bin/bash
# 🔁 Self-saving script: 10-second Alive Pinger for RBOTzilla

FILE="rbotzilla_alive_ping.sh"

cat << 'EOF' > "$FILE"
#!/bin/bash
# 🟢 RBOTzilla Alive Ping — Real-Time Bot Check-in Every 10 Seconds

COLORS=(32 33 34 35 36 91 92 93 94 95)
COLOR_INDEX=0

while true; do
  COLOR=${COLORS[$COLOR_INDEX]}
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo -e "\033[1;${COLOR}m🟢 Message_from_Health_Ping [${TIMESTAMP}]: RBOTzilla is alive and idle. No trades right now.\033[0m"
  echo ""
  COLOR_INDEX=$(( (COLOR_INDEX + 1) % ${#COLORS[@]} ))
  sleep 10
done
EOF

chmod +x "$FILE"
echo "✅ Alive ping script saved as: $FILE"
echo "📡 Launch it with: ./$FILE"
