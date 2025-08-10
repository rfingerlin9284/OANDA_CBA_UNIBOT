#!/usr/bin/env python3
"""Daily Growth Tracker - $400/day Progress Monitor"""
import json
import os
from datetime import datetime, timedelta

class DailyGrowthTracker:
    def __init__(self):
        self.daily_target = 400.0
        self.growth_log_file = 'logs/daily_growth.json'
        self.ensure_log_file()
        
    def ensure_log_file(self):
        """Create growth log file if it doesn't exist"""
        os.makedirs('logs', exist_ok=True)
        if not os.path.exists(self.growth_log_file):
            with open(self.growth_log_file, 'w') as f:
                json.dump({}, f)
    
    def log_daily_performance(self, realized_pnl, unrealized_pnl, trade_count):
        """
        📅 DAILY GROWTH TRACKING
        Fixes: No tracking of net growth toward $400/day goal
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Load existing data
        with open(self.growth_log_file, 'r') as f:
            growth_data = json.load(f)
        
        # Update today's data
        if today not in growth_data:
            growth_data[today] = {
                'target': self.daily_target,
                'realized_pnl': 0.0,
                'unrealized_pnl': 0.0,
                'trade_count': 0,
                'last_update': datetime.now().isoformat()
            }
        
        growth_data[today]['realized_pnl'] = realized_pnl
        growth_data[today]['unrealized_pnl'] = unrealized_pnl
        growth_data[today]['trade_count'] = trade_count
        growth_data[today]['last_update'] = datetime.now().isoformat()
        
        # Save updated data
        with open(self.growth_log_file, 'w') as f:
            json.dump(growth_data, f, indent=2)
        
        # Display progress
        self.display_growth_status(growth_data[today])
        
        # Check for audit triggers
        self.check_audit_triggers(growth_data)
    
    def display_growth_status(self, today_data):
        """Display real-time growth progress"""
        total_pnl = today_data['realized_pnl'] + today_data['unrealized_pnl']
        progress_pct = (total_pnl / self.daily_target) * 100
        remaining = self.daily_target - total_pnl
        
        # Color coding
        if progress_pct >= 100:
            color = '\033[92m'  # Green - Target reached
        elif progress_pct >= 50:
            color = '\033[93m'  # Yellow - Halfway there
        else:
            color = '\033[91m'  # Red - Behind target
        
        print(f"\n{color}╔════════════════════════════════════════════╗\033[0m")
        print(f"{color}║            DAILY GROWTH TRACKER            ║\033[0m")
        print(f"{color}╠════════════════════════════════════════════╣\033[0m")
        print(f"{color}║ Target:      ${self.daily_target:>8.2f}             ║\033[0m")
        print(f"{color}║ Realized:    ${today_data['realized_pnl']:>8.2f}             ║\033[0m")
        print(f"{color}║ Unrealized:  ${today_data['unrealized_pnl']:>8.2f}             ║\033[0m")
        print(f"{color}║ Total:       ${total_pnl:>8.2f}             ║\033[0m")
        print(f"{color}║ Progress:    {progress_pct:>7.1f}%              ║\033[0m")
        print(f"{color}║ Remaining:   ${remaining:>8.2f}             ║\033[0m")
        print(f"{color}║ Trades:      {today_data['trade_count']:>8}               ║\033[0m")
        print(f"{color}╚════════════════════════════════════════════╝\033[0m\n")
    
    def check_audit_triggers(self, growth_data):
        """Check for profit audit triggers"""
        # Get last 3 days
        recent_days = []
        for i in range(3):
            day = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            if day in growth_data:
                recent_days.append(growth_data[day])
        
        if len(recent_days) >= 3:
            underperforming_days = sum(1 for day in recent_days 
                                     if (day['realized_pnl'] + day['unrealized_pnl']) < self.daily_target)
            
            if underperforming_days >= 3:
                print(f"\n🚨 PROFIT AUDIT TRIGGERED!")
                print(f"💡 {underperforming_days}/3 recent days below ${self.daily_target} target")
                print(f"🔍 Recommendation: Run hourly_audit_runner.py for analysis")
                
                # Log audit trigger
                with open('logs/audit_triggers.log', 'a') as f:
                    f.write(f"{datetime.now()} - Profit audit triggered: {underperforming_days}/3 days below target\n")

    """Test daily growth tracking"""
    tracker = DailyGrowthTracker()
    
    # Simulate daily performance
    tracker.log_daily_performance(
        realized_pnl=125.75,
        unrealized_pnl=-15.25,
        trade_count=8
    )

if __name__ == "__main__":
