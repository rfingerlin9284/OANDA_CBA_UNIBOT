#!/bin/bash
# Enhanced Swarm Performance Monitor

echo "📊 ENHANCED SWARM PERFORMANCE MONITOR"
echo "===================================="

# Check if bot is running
if pgrep -f "main_swarm_enhanced.py" > /dev/null; then
    echo "✅ Enhanced Swarm Bot is RUNNING"
    
    # Show recent performance
    echo ""
    echo "📈 Recent Performance Reports:"
    ls -lt performance_reports/enhanced_swarm_performance_*.json 2>/dev/null | head -5
    
    # Show log tail
    echo ""
    echo "📝 Recent Log Activity:"
    tail -10 logs/enhanced_swarm.log 2>/dev/null || echo "No logs found yet"
    
else
    echo "❌ Enhanced Swarm Bot is NOT RUNNING"
    echo ""
    echo "To start the bot, run:"
    echo "./start_enhanced_swarm.sh"
fi

