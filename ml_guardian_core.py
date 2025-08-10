#!/usr/bin/env python3
# 🔮 ML Guardian Core - Integrated smart trading system
# Combines all ML guardian components for empire-wide deployment

import logging
from datetime import datetime
import json
import os

from ml_decision_filter import MLDecisionFilter
from smart_realloc_agent import SmartReallocAgent
from bad_strategy_detector import BadStrategyDetector

class MLGuardianCore:
    def __init__(self, platform_name="UNKNOWN"):
        self.platform_name = platform_name
        self.decision_filter = MLDecisionFilter()
        self.realloc_agent = SmartReallocAgent()
        self.strategy_detector = BadStrategyDetector()
        
        # Performance tracking
        self.guardian_stats = {
            'trades_approved': 0,
            'trades_rejected': 0,
            'reallocations_executed': 0,
            'strategies_disabled': 0,
            'total_fees_saved': 0,
            'net_pnl_improvement': 0
        }
        
        self.setup_logging()
    
    def setup_logging(self):
        """Setup ML Guardian logging"""
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'ml_guardian_{datetime.now().strftime("%Y%m%d")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        logging.info(f"🧠 ML GUARDIAN CORE INITIALIZED: {self.platform_name}")
    
    def evaluate_trade(self, prediction, symbol, fee_estimate, ml_model=None, router=None):
        """
        Complete trade evaluation pipeline
        Returns: (execute: bool, reason: str, adjusted_prediction: dict)
        """
        try:
            # Step 1: Check if strategy is enabled
            strategy_id = prediction.get('strategy_id', 'default')
            
            if not self.strategy_detector.is_strategy_enabled(strategy_id):
                reason = f"🚫 STRATEGY DISABLED: {strategy_id}"
                logging.warning(f"Trade blocked - {reason}")
                self.guardian_stats['trades_rejected'] += 1
                return False, reason, prediction
            
            # Step 2: ML Decision Filter
            approved, filter_reason, adjusted_prediction = self.decision_filter.approve_trade(
                prediction, fee_estimate, symbol
            )
            
            if not approved:
                self.guardian_stats['trades_rejected'] += 1
                self.guardian_stats['total_fees_saved'] += fee_estimate
                return False, filter_reason, adjusted_prediction
            
            # Step 3: Final approval
            self.guardian_stats['trades_approved'] += 1
            
            enhanced_reason = f"✅ ML GUARDIAN APPROVED: {filter_reason}"
            logging.info(f"Trade approved - {enhanced_reason}")
            
            return True, enhanced_reason, adjusted_prediction
            
        except Exception as e:
            error_reason = f"❌ ML GUARDIAN ERROR: {str(e)}"
            logging.error(error_reason)
            return False, error_reason, prediction
    
    def handle_trade_result(self, trade_data, result, pnl=0, ml_model=None, router=None):
        """
        Handle trade completion and trigger reallocation if needed
        Args:
            trade_data: Original trade information
            result: 'SUCCESS', 'FAILURE', 'KILLED'
            pnl: Profit/loss amount
            ml_model: ML model for reallocation
            router: Trading router for execution
        """
        try:
            strategy_id = trade_data.get('strategy_id', 'default')
            symbol = trade_data.get('symbol', 'UNKNOWN')
            
            # Track strategy performance
            self.strategy_detector.track_strategy_result(strategy_id, symbol, result, pnl)
            
            # Handle trade killing and reallocation
            if result == 'KILLED' or (result == 'FAILURE' and pnl < -100):
                trade_data['kill_reason'] = 'Poor performance' if result == 'FAILURE' else 'Manual kill'
                
                success, new_trades, realloc_reason = self.realloc_agent.reallocate_on_kill(
                    trade_data, ml_model, router
                )
                
                if success:
                    self.guardian_stats['reallocations_executed'] += 1
                    self.guardian_stats['net_pnl_improvement'] += abs(pnl) * 0.5  # Estimate improvement
                    
                logging.info(f"Trade result handled: {symbol} {result} - {realloc_reason}")
            
            # Update PnL tracking
            if pnl != 0:
                self.guardian_stats['net_pnl_improvement'] += pnl
                
        except Exception as e:
            logging.error(f"Error handling trade result: {e}")
    
    def get_guardian_dashboard(self):
        """Generate comprehensive guardian dashboard"""
        filter_stats = self.decision_filter.get_rejection_stats()
        realloc_stats = self.realloc_agent.get_reallocation_stats()
        strategy_stats = self.strategy_detector.get_strategy_stats()
        
        dashboard = {
            'platform': self.platform_name,
            'timestamp': datetime.now().isoformat(),
            'guardian_stats': self.guardian_stats,
            'decision_filter': filter_stats,
            'reallocation': realloc_stats,
            'strategy_monitoring': strategy_stats,
            'performance_summary': {
                'approval_rate': self.guardian_stats['trades_approved'] / 
                               (self.guardian_stats['trades_approved'] + self.guardian_stats['trades_rejected'])
                               if (self.guardian_stats['trades_approved'] + self.guardian_stats['trades_rejected']) > 0 else 0,
                'fees_saved': self.guardian_stats['total_fees_saved'],
                'net_improvement': self.guardian_stats['net_pnl_improvement'],
                'active_strategies': strategy_stats['total_strategies'] - strategy_stats['disabled_strategies']
            }
        }
        
        return dashboard
    
    def save_guardian_report(self):
        """Save guardian performance report"""
        dashboard = self.get_guardian_dashboard()
        
        report_file = f'ml_guardian_report_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
        
        with open(report_file, 'w') as f:
            json.dump(dashboard, f, indent=2)
        
        logging.info(f"Guardian report saved: {report_file}")
        return report_file

# Global guardian instance for easy access
ml_guardian = None

def get_ml_guardian(platform_name="OANDA"):
    """Get or create ML Guardian instance"""
    global ml_guardian
    if ml_guardian is None:
        ml_guardian = MLGuardianCore(platform_name)
    return ml_guardian
