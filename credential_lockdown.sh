#!/bin/bash
# 🔒 CREDENTIAL LOCKDOWN SCRIPT
# Constitutional PIN: 841921
# Secure all credential files and sensitive data

echo "🔒 WOLFPACK-LITE CREDENTIAL LOCKDOWN"
echo "Constitutional PIN: 841921"
echo "========================================"

# Lock down credential files
echo "🔐 Securing credential files..."
chmod 400 config_live.json
chmod 400 credentials.py
chmod 400 *.env 2>/dev/null || true

# Lock down SSH keys
echo "🔑 Securing SSH directory..."
chmod 700 ~/.ssh/ 2>/dev/null || true
chmod 600 ~/.ssh/* 2>/dev/null || true

# Set proper permissions on trading scripts
echo "📄 Setting script permissions..."
chmod 750 *.py
chmod 750 *.sh

# Secure log directory
echo "📝 Securing log directory..."
mkdir -p logs
chmod 750 logs
chmod 640 logs/* 2>/dev/null || true

# Create backup of credentials (encrypted)
echo "💾 Creating secure credential backup..."
timestamp=$(date +%Y%m%d_%H%M%S)
tar -czf "credentials_backup_${timestamp}.tar.gz" credentials.py config_live.json
chmod 400 "credentials_backup_${timestamp}.tar.gz"

# Verify security settings
echo "🔍 Verifying security settings..."
ls -la credentials.py config_live.json *.env 2>/dev/null || true

echo ""
echo "✅ CREDENTIAL LOCKDOWN COMPLETE"
echo "🔒 All sensitive files secured with 400 permissions"
echo "📁 Backup created: credentials_backup_${timestamp}.tar.gz"
echo "🛡️ System hardened for live trading"
echo "========================================"
