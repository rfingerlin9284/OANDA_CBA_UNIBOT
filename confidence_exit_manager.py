#!/usr/bin/env python3
"""Confidence-Based Exit Manager - Dynamic Exits Based on ML Feedback"""
import time
from datetime import datetime, timedelta

class ConfidenceExitManager:
    def __init__(self):
        self.confidence_drop_threshold = 0.15  # 15% confidence drop triggers exit
        self.min_hold_time = 300  # 5 minutes minimum hold
        self.max_hold_time = 1800  # 30 minutes maximum hold
        self.active_trades = {}
        
    def should_exit_trade(self, trade_id, current_ml_confidence, entry_confidence, 
                         entry_time, current_pnl, current_pnl_pct):
        """
        🧠 CONFIDENCE-BASED EXITS
        Fixes: Exiting at +$0.21, +$0.89 profits or holding losers too long
        """
        time_in_market = (datetime.now() - entry_time).total_seconds()
        confidence_drop = entry_confidence - current_ml_confidence
        
        print(f"🧠 CONFIDENCE EXIT ANALYSIS:")
        print(f"   Trade ID: {trade_id}")
        print(f"   Entry Confidence: {entry_confidence:.1%}")
        print(f"   Current Confidence: {current_ml_confidence:.1%}")
        print(f"   Confidence Drop: {confidence_drop:.1%}")
        print(f"   Time in Market: {time_in_market/60:.1f} minutes")
        print(f"   Current P&L: ${current_pnl:.2f} ({current_pnl_pct:.2%})")
        
        # Exit conditions
        exit_decisions = []
        
        # 1. Confidence Drop Exit (High Priority)
        if confidence_drop > self.confidence_drop_threshold:
            exit_decisions.append({
                'reason': f'Confidence dropped {confidence_drop:.1%} > {self.confidence_drop_threshold:.1%}',
                'priority': 'HIGH',
                'action': 'EXIT_NOW'
            })
        
        # 2. Time-Based Exits
        if time_in_market > self.max_hold_time:
            if current_pnl < 0:
                exit_decisions.append({
                    'reason': f'Max time reached ({self.max_hold_time/60:.0f}min) with loss',
                    'priority': 'HIGH',
                    'action': 'EXIT_NOW'
                })
            elif abs(current_pnl) < 5:  # Break-even
                exit_decisions.append({
                    'reason': f'Max time reached with minimal P&L',
                    'priority': 'MEDIUM',
                    'action': 'EXIT_BREAKEVEN'
                })
        
        # 3. Profit-Taking Logic Based on Confidence
        if current_pnl > 0:
            if entry_confidence > 0.90:
                # High confidence: Let it run longer, take bigger profits
                if current_pnl > 25 or current_pnl_pct > 0.015:  # $25 or 1.5%
                    exit_decisions.append({
                        'reason': f'High confidence profit target: ${current_pnl:.2f}',
                        'priority': 'MEDIUM',
                        'action': 'TAKE_PROFIT'
                    })
            else:
                # Lower confidence: Take smaller profits quickly
                if current_pnl > 10 or current_pnl_pct > 0.008:  # $10 or 0.8%
                    exit_decisions.append({
                        'reason': f'Quick profit on lower confidence: ${current_pnl:.2f}',
                        'priority': 'MEDIUM',
                        'action': 'TAKE_PROFIT'
                    })
        
        # 4. Loss-Cutting Logic
        elif current_pnl < 0:
            if current_ml_confidence < 0.70:  # Low current confidence
                exit_decisions.append({
                    'reason': f'Cut loss with low confidence: {current_ml_confidence:.1%}',
                    'priority': 'HIGH',
                    'action': 'CUT_LOSS'
                })
        
        # 5. Hold Decision
        if not exit_decisions and time_in_market > self.min_hold_time:
            exit_decisions.append({
                'reason': f'Continue holding - confidence stable at {current_ml_confidence:.1%}',
                'priority': 'LOW',
                'action': 'HOLD'
            })
        
        # Return highest priority decision
        if exit_decisions:
            best_decision = max(exit_decisions, 
                              key=lambda x: {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[x['priority']])
            
            color = '\033[91m' if best_decision['action'].startswith('EXIT') else \
                   '\033[92m' if best_decision['action'] == 'TAKE_PROFIT' else '\033[93m'
            
            print(f"{color}🎯 DECISION: {best_decision['action']}\033[0m")
            print(f"   Reason: {best_decision['reason']}")
            print(f"   Priority: {best_decision['priority']}")
            
            return best_decision['action'] != 'HOLD', best_decision
        
        return False, {'action': 'HOLD', 'reason': 'No exit conditions met'}

    """Test confidence-based exit logic"""
    manager = ConfidenceExitManager()
    
        {
            'trade_id': 'TEST1',
            'current_ml_confidence': 0.60,
            'entry_confidence': 0.85,
            'entry_time': datetime.now() - timedelta(minutes=20),
            'current_pnl': -8.5,
            'current_pnl_pct': -0.005
        },
        {
            'trade_id': 'TEST2',
            'current_ml_confidence': 0.92,
            'entry_confidence': 0.95,
            'entry_time': datetime.now() - timedelta(minutes=15),
            'current_pnl': 28.7,
            'current_pnl_pct': 0.018
        }
    ]
    
        print(f"\n🧪 Testing scenario: {scenario['trade_id']}")
        should_exit, decision = manager.should_exit_trade(**scenario)
        print()

if __name__ == "__main__":
