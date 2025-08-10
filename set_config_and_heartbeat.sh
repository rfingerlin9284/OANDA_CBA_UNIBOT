
#!/bin/bash
cd ~/FOUR_horsemen/ALPHA_FOUR/proto_oanda/wolfpack-lite
cat > config.json <<EOF
{
  "heartbeat_interval": 20,
  "log_path": "logs/health/heartbeat.log"
}
EOF
mkdir -p logs/health
touch logs/health/heartbeat.log
echo "[✅] Config and heartbeat log initialized."
EOF
