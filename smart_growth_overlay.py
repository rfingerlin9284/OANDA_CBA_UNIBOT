#!/usr/bin/env python3
"""
🚀 SMART PROFIT GROWTH OVERLAY 🚀
Real-time monitoring and optimization for OANDA profit growth

CONSTITUTIONAL PIN: 841921
ACTIVE OVERLAY: Runs continuously to optimize profit growth
"""

import json
import time
import threading
import datetime
import logging
import os
import sys
from typing import Dict, List, Optional

# Add current directory to path
sys.path.append('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda')

from inject_smart_profit_growth_mode import SmartProfitGrowthEngine

# Setup dedicated growth overlay logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - GROWTH_OVERLAY - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/growth_overlay.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SmartGrowthOverlay:
    """
    🔄 Real-time overlay that continuously optimizes profit growth
    """
    def __init__(self):
        self.growth_engine = SmartProfitGrowthEngine()
        self.is_running = False
        self.monitor_thread = None
        
        # Monitoring intervals
        self.position_check_interval = 30  # seconds
        self.pnl_update_interval = 300     # 5 minutes
        self.allocation_update_interval = 3600  # 1 hour
        
        # Current positions tracking
        self.active_positions = {}
        self.position_entry_times = {}
        self.position_entry_confidence = {}
        
    def start_overlay(self):
        """Start the growth overlay monitoring"""
        if self.is_running:
            logger.warning("⚠️ Growth overlay already running")
            return
            
        self.is_running = True
        logger.info("🚀 Starting Smart Profit Growth Overlay")
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # Start P&L tracking thread
        pnl_thread = threading.Thread(target=self._pnl_tracking_loop, daemon=True)
        pnl_thread.start()
        
        # Start allocation optimization thread
        allocation_thread = threading.Thread(target=self._allocation_loop, daemon=True)
        allocation_thread.start()
        
        logger.info("✅ All growth overlay threads started")

    def stop_overlay(self):
        """Stop the growth overlay"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("🛑 Smart Profit Growth Overlay stopped")

    def _monitor_loop(self):
        """Main monitoring loop for positions"""
        logger.info("🔍 Position monitoring loop started")
        
        while self.is_running:
            try:
                self._check_active_positions()
                self._monitor_position_exits()
                time.sleep(self.position_check_interval)
            except Exception as e:
                logger.error(f"❌ Error in position monitoring: {e}")
                time.sleep(5)

    def _pnl_tracking_loop(self):
        """P&L tracking and daily target monitoring"""
        logger.info("💰 P&L tracking loop started")
        
        while self.is_running:
            try:
                current_pnl = self._get_current_daily_pnl()
                self.growth_engine.track_daily_pnl(current_pnl)
                time.sleep(self.pnl_update_interval)
            except Exception as e:
                logger.error(f"❌ Error in P&L tracking: {e}")
                time.sleep(30)

    def _allocation_loop(self):
        """Capital allocation optimization loop"""
        logger.info("📊 Allocation optimization loop started")
        
        while self.is_running:
            try:
                self.growth_engine.update_capital_allocation()
                self.growth_engine.save_growth_state()
                time.sleep(self.allocation_update_interval)
            except Exception as e:
                logger.error(f"❌ Error in allocation optimization: {e}")
                time.sleep(60)

    def _check_active_positions(self):
        """Check and update active positions"""
        try:
            # Simulate position check (integrate with your OANDA API)
            positions_file = '/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/data/current_positions.json'
            
            if os.path.exists(positions_file):
                with open(positions_file, 'r') as f:
                    positions = json.load(f)
                    
                # Update active positions tracking
                for position in positions.get('positions', []):
                    pair = position.get('instrument')
                    units = position.get('units', 0)
                    
                    if pair and abs(units) > 0:
                        self.active_positions[pair] = position
                        
                        # Track entry time if new position
                        if pair not in self.position_entry_times:
                            self.position_entry_times[pair] = datetime.datetime.now()
                            
                        # Update JPY tracking
                        if pair in self.growth_engine.jpy_pairs:
                            self.growth_engine.active_jpy_positions.add(pair)
                    else:
                        # Position closed
                        if pair in self.active_positions:
                            del self.active_positions[pair]
                        if pair in self.position_entry_times:
                            del self.position_entry_times[pair]
                        if pair in self.position_entry_confidence:
                            del self.position_entry_confidence[pair]
                        if pair in self.growth_engine.active_jpy_positions:
                            self.growth_engine.active_jpy_positions.remove(pair)
                            
            else:
                logger.warning("⚠️ No positions file found")
                
        except Exception as e:
            logger.error(f"❌ Error checking positions: {e}")

    def _monitor_position_exits(self):
        """Monitor positions for early exit conditions"""
        for pair, position in self.active_positions.items():
            try:
                # Get current confidence (liveulate - integrate with your ML model)
                current_confidence = self._get_current_confidence(pair)
                entry_confidence = self.position_entry_confidence.get(pair, 0.8)
                
                # Calculate time in market
                entry_time = self.position_entry_times.get(pair, datetime.datetime.now())
                time_in_market = (datetime.datetime.now() - entry_time).total_seconds() / 60  # minutes
                
                # Check exit conditions
                should_exit = self.growth_engine.should_exit_early(
                    pair, current_confidence, entry_confidence, time_in_market
                )
                
                if should_exit:
                    logger.warning(f"🚨 Early exit recommended for {pair}")
                    self._trigger_position_exit(pair, "GROWTH_ENGINE_EXIT")
                    
            except Exception as e:
                logger.error(f"❌ Error monitoring exit for {pair}: {e}")

    def _get_current_daily_pnl(self) -> float:
        """Get current daily P&L"""
        try:
            # Read from your P&L tracking system
            pnl_file = '/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/data/daily_pnl.json'
            if os.path.exists(pnl_file):
                with open(pnl_file, 'r') as f:
                    pnl_data = json.load(f)
                    return pnl_data.get('current_daily_pnl', 0.0)
            
            # Fallback: calculate from positions
            total_pnl = 0.0
            for pair, position in self.active_positions.items():
                unrealized_pnl = position.get('unrealizedPL', 0)
                if unrealized_pnl:
                    total_pnl += float(unrealized_pnl)
                    
            return total_pnl
            
        except Exception as e:
            logger.error(f"❌ Error getting daily P&L: {e}")
            return 0.0

    def _get_current_confidence(self, pair: str) -> float:
        """Get current ML model confidence for pair"""
        try:
            # Integrate with your ML model confidence system
            confidence_file = f'/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/data/confidence_{pair}.json'
            if os.path.exists(confidence_file):
                with open(confidence_file, 'r') as f:
                    conf_data = json.load(f)
                    return conf_data.get('current_confidence', 0.5)
            
            # Default confidence
            return 0.7
            
        except Exception as e:
            logger.error(f"❌ Error getting confidence for {pair}: {e}")
            return 0.5

    def _trigger_position_exit(self, pair: str, reason: str):
        """Trigger position exit with reason"""
        try:
            # Create exit signal file
            exit_signal = {
                'pair': pair,
                'action': 'CLOSE_POSITION',
                'reason': reason,
                'timestamp': datetime.datetime.now().isoformat(),
                'source': 'SMART_GROWTH_OVERLAY'
            }
            
            exit_file = f'/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/signals/exit_{pair}_{int(time.time())}.json'
            os.makedirs(os.path.dirname(exit_file), exist_ok=True)
            
            with open(exit_file, 'w') as f:
                json.dump(exit_signal, f, indent=2)
                
            logger.info(f"📤 Exit signal created for {pair}: {reason}")
            
        except Exception as e:
            logger.error(f"❌ Error creating exit signal for {pair}: {e}")

    def get_overlay_status(self) -> Dict:
        """Get current overlay status"""
        return {
            'is_running': self.is_running,
            'active_positions': len(self.active_positions),
            'jpy_pairs_active': len(self.growth_engine.active_jpy_positions),
            'last_check': datetime.datetime.now().isoformat(),
            'target_daily_profit': self.growth_engine.target_daily_profit,
            'current_daily_pnl': self._get_current_daily_pnl()
        }

def main():
    """Main function to start the overlay"""
    print("🚀 SMART PROFIT GROWTH OVERLAY")
    print("=" * 50)
    print("Constitutional PIN: 841921")
    print("Real-time profit optimization for OANDA")
    print()
    
    overlay = SmartGrowthOverlay()
    
    try:
        overlay.start_overlay()
        print("✅ Growth overlay started successfully")
        print("🔄 Monitoring active...")
        print("📊 Press Ctrl+C to stop")
        
        # Keep running
        while True:
            status = overlay.get_overlay_status()
            print(f"\r💰 Daily P&L: ${status['current_daily_pnl']:.2f} | Active: {status['active_positions']} | JPY: {status['jpy_pairs_active']}", end='', flush=True)
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping growth overlay...")
        overlay.stop_overlay()
        print("✅ Overlay stopped")

if __name__ == "__main__":
    main()
