#!/bin/bash
# OANDA TOKEN REPLACEMENT SCRIPT
# Run this after getting your NEW token from OANDA

set -e

echo "🔄 OANDA TOKEN REPLACEMENT UTILITY"
echo "=================================="
echo ""
echo "⚠️  Your current token is INVALID/EXPIRED:"
echo "   9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
echo ""
echo "🔑 You need to:"
echo "   1. Login to your OANDA account"
echo "   2. Go to API Management"
echo "   3. Generate a NEW API token"
echo "   4. Come back and run: ./replace_token.sh YOUR_NEW_TOKEN"
echo ""

if [ -z "$1" ]; then
    echo "❌ Usage: ./replace_token.sh YOUR_NEW_OANDA_TOKEN"
    echo ""
    echo "📝 Example:"
    echo "   ./replace_token.sh abc123def456ghi789-new-token-here"
    exit 1
fi

NEW_TOKEN="$1"
OLD_TOKEN="9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"

echo "🔄 Replacing OANDA token in all files..."

# Replace in all Python files
find . -name "*.py" -type f -exec sed -i "s/$OLD_TOKEN/$NEW_TOKEN/g" {} \;

# Replace in all JSON files
find . -name "*.json" -type f -exec sed -i "s/$OLD_TOKEN/$NEW_TOKEN/g" {} \;

# Replace in all shell scripts
find . -name "*.sh" -type f -exec sed -i "s/$OLD_TOKEN/$NEW_TOKEN/g" {} \;

# Replace in markdown files
find . -name "*.md" -type f -exec sed -i "s/$OLD_TOKEN/$NEW_TOKEN/g" {} \;

echo "✅ Token replacement complete!"
echo ""
echo "🧪 Testing new token..."

# Test the new token
curl -s -H "Authorization: Bearer $NEW_TOKEN" "https://api-fxtrade.oanda.com/v3/accounts" > /tmp/token_test.json

if grep -q "errorMessage" /tmp/token_test.json; then
    echo "❌ NEW TOKEN FAILED:"
    cat /tmp/token_test.json
    echo ""
    echo "⚠️  Make sure you:"
    echo "   - Generated the token for LIVE trading (not practice)"
    echo "   - Copied the FULL token including all characters"
    echo "   - Have trading permissions enabled"
else
    echo "✅ NEW TOKEN WORKS!"
    echo ""
    echo "🚀 Ready to start live trading:"
    echo "   source coinbase_env/bin/activate"
    echo "   python3 live_trading_main.py"
fi

rm -f /tmp/token_test.json
