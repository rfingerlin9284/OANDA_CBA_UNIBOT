#!/usr/bin/env python3
# 🎯 Bad Strategy Detection - Auto-disable failing strategies
# Monitors strategy performance and disables consistently failing ones

import logging
from datetime import datetime, timedelta
import json

class BadStrategyDetector:
    def __init__(self, failure_threshold=3, monitoring_window_hours=24):
        self.failure_threshold = failure_threshold
        self.monitoring_window = timedelta(hours=monitoring_window_hours)
        self.strategy_performance = {}
        self.disabled_strategies = set()
        
    def track_strategy_result(self, strategy_id, symbol, result, pnl=0):
        """
        Track strategy performance for auto-disabling
        Args:
            strategy_id: Strategy identifier
            symbol: Trading pair
            result: 'SUCCESS', 'FAILURE', 'NEUTRAL'
            pnl: Profit/loss amount
        """
        timestamp = datetime.now()
        
        if strategy_id not in self.strategy_performance:
            self.strategy_performance[strategy_id] = {
                'trades': [],
                'total_pnl': 0,
                'success_count': 0,
                'failure_count': 0
            }
        
        # Add trade record
        trade_record = {
            'timestamp': timestamp,
            'symbol': symbol,
            'result': result,
            'pnl': pnl
        }
        
        self.strategy_performance[strategy_id]['trades'].append(trade_record)
        self.strategy_performance[strategy_id]['total_pnl'] += pnl
        
        if result == 'SUCCESS':
            self.strategy_performance[strategy_id]['success_count'] += 1
        elif result == 'FAILURE':
            self.strategy_performance[strategy_id]['failure_count'] += 1
        
        # Clean old trades outside monitoring window
        self.cleanup_old_trades(strategy_id, timestamp)
        
        # Check if strategy should be disabled
        self.check_strategy_health(strategy_id)
        
    def cleanup_old_trades(self, strategy_id, current_time):
        """Remove trades outside the monitoring window"""
        cutoff_time = current_time - self.monitoring_window
        
        trades = self.strategy_performance[strategy_id]['trades']
        valid_trades = [t for t in trades if t['timestamp'] > cutoff_time]
        
        # Recalculate counts for valid trades only
        success_count = len([t for t in valid_trades if t['result'] == 'SUCCESS'])
        failure_count = len([t for t in valid_trades if t['result'] == 'FAILURE'])
        total_pnl = sum(t['pnl'] for t in valid_trades)
        
        self.strategy_performance[strategy_id].update({
            'trades': valid_trades,
            'success_count': success_count,
            'failure_count': failure_count,
            'total_pnl': total_pnl
        })
    
    def check_strategy_health(self, strategy_id):
        """Check if strategy should be disabled due to poor performance"""
        if strategy_id in self.disabled_strategies:
            return  # Already disabled
        
        perf = self.strategy_performance[strategy_id]
        
        # Check consecutive failures
        recent_trades = perf['trades'][-self.failure_threshold:]
        if len(recent_trades) >= self.failure_threshold:
            consecutive_failures = all(t['result'] == 'FAILURE' for t in recent_trades)
            
            if consecutive_failures:
                self.disable_strategy(strategy_id, f"Consecutive failures: {self.failure_threshold}")
                return
        
        # Check failure rate in monitoring window
        total_trades = len(perf['trades'])
        if total_trades >= 10:  # Minimum trades for statistical significance
            failure_rate = perf['failure_count'] / total_trades
            
            if failure_rate > 0.7:  # 70% failure rate
                self.disable_strategy(strategy_id, f"High failure rate: {failure_rate:.1%}")
                return
        
        # Check negative PnL threshold
        if perf['total_pnl'] < -1000:  # Adjust threshold as needed
            self.disable_strategy(strategy_id, f"Excessive losses: ${perf['total_pnl']:.2f}")
            return
    
    def disable_strategy(self, strategy_id, reason):
        """Disable a poorly performing strategy"""
        self.disabled_strategies.add(strategy_id)
        
        log_msg = f"🚫 STRATEGY DISABLED: {strategy_id} - {reason}"
        logging.warning(log_msg)
        
        # Save disabled strategy info
        with open('disabled_strategies.json', 'w') as f:
            disabled_info = {
                'strategies': list(self.disabled_strategies),
                'last_updated': datetime.now().isoformat(),
                'reasons': {strategy_id: reason}
            }
            json.dump(disabled_info, f, indent=2)
    
    def is_strategy_enabled(self, strategy_id):
        """Check if strategy is currently enabled"""
        return strategy_id not in self.disabled_strategies
    
    def enable_strategy(self, strategy_id):
        """Re-enable a previously disabled strategy"""
        if strategy_id in self.disabled_strategies:
            self.disabled_strategies.remove(strategy_id)
            logging.info(f"✅ STRATEGY RE-ENABLED: {strategy_id}")
            
            # Reset performance tracking for fresh start
            if strategy_id in self.strategy_performance:
                self.strategy_performance[strategy_id] = {
                    'trades': [],
                    'total_pnl': 0,
                    'success_count': 0,
                    'failure_count': 0
                }
    
    def get_strategy_stats(self):
        """Get comprehensive strategy performance statistics"""
        stats = {
            'total_strategies': len(self.strategy_performance),
            'disabled_strategies': len(self.disabled_strategies),
            'strategy_details': {}
        }
        
        for strategy_id, perf in self.strategy_performance.items():
            total_trades = len(perf['trades'])
            success_rate = perf['success_count'] / total_trades if total_trades > 0 else 0
            
            stats['strategy_details'][strategy_id] = {
                'enabled': strategy_id not in self.disabled_strategies,
                'total_trades': total_trades,
                'success_rate': success_rate,
                'total_pnl': perf['total_pnl'],
                'recent_trades': len([t for t in perf['trades'] if t['timestamp'] > datetime.now() - timedelta(hours=6)])
            }
        
        return stats
