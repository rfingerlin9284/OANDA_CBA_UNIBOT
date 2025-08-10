#!/usr/bin/env python3
"""Profit Gating with Time-in-Market Enforcement"""
import time
from datetime import datetime, timedelta

class ProfitGatingManager:
    def __init__(self):
        self.active_trades = {}
        self.max_time_breakeven = 1800  # 30 minutes
        self.profit_lock_threshold = 0.003  # 0.3%
        
    def should_take_profit(self, trade_data):
        """
        💰 PROFIT GATING: Enhanced profit-taking logic
        Enforces time limits and dynamic profit thresholds
        """
        trade_id = trade_data.get('id')
        unrealized_pnl = trade_data.get('unrealized_pl', 0)
        entry_price = trade_data.get('entry_price', 0)
        current_price = trade_data.get('current_price', 0)
        fees = trade_data.get('fees', 5.0)  # Estimated $5 spread/commission
        entry_time = trade_data.get('entry_time', datetime.now())
        
        # Calculate P&L percentage
        if entry_price > 0:
            pnl_pct = abs(current_price - entry_price) / entry_price
        else:
            pnl_pct = 0
        
        time_in_market = (datetime.now() - entry_time).total_seconds()
        
        # Track trade
        if trade_id not in self.active_trades:
            self.active_trades[trade_id] = {
                'entry_time': entry_time,
                'max_profit': unrealized_pnl,
                'profit_alerts': 0
            }
        
        trade_info = self.active_trades[trade_id]
        
        # Update max profit
        if unrealized_pnl > trade_info['max_profit']:
            trade_info['max_profit'] = unrealized_pnl
        
        # Decision logic
        decisions = []
        
        # 1. Profit threshold reached
        if unrealized_pnl >= fees * 3:
            decisions.append({
                'action': 'TAKE_PROFIT',
                'reason': f'Profit target: ${unrealized_pnl:.2f} vs ${fees * 3:.2f} threshold',
                'priority': 'HIGH'
            })
        
        # 2. Time-in-market limit for break-even trades
        elif time_in_market > self.max_time_breakeven and abs(unrealized_pnl) < fees:
            decisions.append({
                'action': 'TIME_EXIT',
                'reason': f'Time limit: {time_in_market/60:.1f} min in break-even',
                'priority': 'MEDIUM'
            })
        
        # 3. Profit lock at 0.3% gain
        elif pnl_pct >= self.profit_lock_threshold and unrealized_pnl > 0:
            decisions.append({
                'action': 'PROFIT_LOCK',
                'reason': f'Profit lock: {pnl_pct:.1%} gain achieved',
                'priority': 'MEDIUM'
            })
        
        # 4. Hold decision
        else:
            decisions.append({
                'action': 'HOLD',
                'reason': f'Continue: ${unrealized_pnl:.2f} P&L, {time_in_market/60:.1f} min',
                'priority': 'LOW'
            })
        
        # Log decision
        for decision in decisions:
            color = '\033[92m' if decision['action'] in ['TAKE_PROFIT', 'PROFIT_LOCK'] else '\033[93m'
            print(f"[PROFIT GATING] {color}{decision['action']}\033[0m: {decision['reason']}")
        
        return decisions

    """Test profit gating system"""
    manager = ProfitGatingManager()
    
        {
            'id': 'TEST1',
            'unrealized_pl': 18.5,
            'entry_price': 1.1000,
            'current_price': 1.1035,
            'fees': 5.0,
            'entry_time': datetime.now() - timedelta(minutes=10)
        },
        {
            'id': 'TEST2', 
            'unrealized_pl': -2.3,
            'entry_price': 1.1000,
            'current_price': 1.0985,
            'fees': 5.0,
            'entry_time': datetime.now() - timedelta(minutes=35)
        }
    ]
    
        print(f"\n🧪 Testing Trade {trade['id']}:")
        decisions = manager.should_take_profit(trade)

if __name__ == "__main__":
