#!/usr/bin/env bash
set -euo pipefail

echo "OANDA Token Update Tool (Secure - NOT stored in repo)"
echo "=================================================="

# Ensure directories exist
mkdir -p ~/fx_guard

# Stop any running processes first
echo "Stopping any running trading processes..."
pkill -f 'place_oanda_order|router|swarm|trade_loop|unibot' || true

# Check current token status
if [ -f ~/fx_guard/.env ]; then
    echo "✓ Found existing environment file"
else
    echo "! No existing environment file found"
fi

# Ask for new token
echo ""
echo "Please paste your OANDA API token from the attachment:"
echo "(Token: ${OANDA_LIVE_API_KEY})"
echo ""
read -r -p "OANDA API Token: " NEW_TOKEN

# Validate token format (basic check)
if [[ ! "$NEW_TOKEN" =~ ^[a-f0-9]{32}-[a-f0-9]{32}$ ]]; then
    echo "⚠ Warning: Token format doesn't match expected pattern"
    read -r -p "Continue anyway? (y/N): " CONTINUE
    if [[ "$CONTINUE" != "y" && "$CONTINUE" != "Y" ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Determine if live or practice
LIVE_URL="https://api-fxtrade.oanda.com"
PRACTICE_URL="https://api-fxpractice.oanda.com"

echo ""
echo "Testing token against OANDA servers..."

# Test live
LIVE_RESULT=$(curl -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $NEW_TOKEN" "$LIVE_URL/v3/accounts" || echo "000")

# Test practice  
PRACTICE_RESULT=$(curl -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $NEW_TOKEN" "$PRACTICE_URL/v3/accounts" || echo "000")

echo "Live API response: $LIVE_RESULT"
echo "Practice API response: $PRACTICE_RESULT"

# Determine which environment
if [[ "$LIVE_RESULT" == "200" ]]; then
    API_URL="$LIVE_URL"
    ENV_TYPE="LIVE"
    echo "✓ Token is valid for LIVE trading"
elif [[ "$PRACTICE_RESULT" == "200" ]]; then
    API_URL="$PRACTICE_URL"
    ENV_TYPE="PRACTICE"  
    echo "✓ Token is valid for PRACTICE trading"
else
    echo "❌ Token failed on both live and practice servers"
    exit 1
fi

# Get account ID
ACCOUNT_JSON=$(curl -sS -H "Authorization: Bearer $NEW_TOKEN" "$API_URL/v3/accounts")
ACCOUNT_ID=$(echo "$ACCOUNT_JSON" | jq -r '.accounts[0].id')

if [[ "$ACCOUNT_ID" == "null" || -z "$ACCOUNT_ID" ]]; then
    echo "❌ Could not retrieve account ID"
    exit 1
fi

echo "✓ Account ID: $ACCOUNT_ID"

# Create secure environment file
cat > ~/fx_guard/.env <<EOF
# OANDA API Configuration - Updated $(date)
# Environment: $ENV_TYPE
OANDA_API_KEY=$NEW_TOKEN
OANDA_ACCOUNT_ID=$ACCOUNT_ID
OANDA_API_URL=$API_URL
OANDA_HOST=$(echo "$API_URL" | sed 's|https://||')

# Legacy variables for compatibility
OANDA_ACCOUNT=$ACCOUNT_ID
OA_KEY=$NEW_TOKEN
OA_ACC=$ACCOUNT_ID
OA_HOST=$(echo "$API_URL" | sed 's|https://||')
EOF

# Secure the file
chmod 600 ~/fx_guard/.env

echo ""
echo "✅ Token updated successfully!"
echo "   Environment: $ENV_TYPE"
echo "   Account: $ACCOUNT_ID"
echo "   Config saved to: ~/fx_guard/.env"
echo ""
echo "Next steps:"
echo "1. Your token is now configured"
echo "2. Run: menu.sh (for main control panel)"
echo "3. Or start trading with: systemctl --user start unibot-auto.service"
