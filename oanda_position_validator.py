#!/usr/bin/env python3
"""
🎯 OANDA POSITION VALIDATOR FOR SMART GROWTH MODE 🎯
Validates all trades before execution using growth mode logic

CONSTITUTIONAL PIN: 841921
INTEGRATION: Works with Smart Profit Growth Mode
"""

import json
import logging
import datetime
import os
import sys
from typing import Dict, Tuple, Optional

# Add current directory to path
sys.path.append('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda')

from inject_smart_profit_growth_mode import SmartProfitGrowthEngine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - POSITION_VALIDATOR - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/position_validator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OandaPositionValidator:
    """
    🔍 Validates all position requests before sending to OANDA
    Enforces Smart Profit Growth Mode rules
    """
    def __init__(self):
        self.growth_engine = SmartProfitGrowthEngine()
        self.validation_rules = {
            'min_rr_ratio': 1.5,
            'max_position_size': 10000,
            'min_position_size': 500,
            'max_spread_threshold': 0.0005,  # 0.5 pips
            'min_confidence_threshold': 0.6
        }
        
    def validate_trade_request(self, trade_request: Dict) -> Tuple[bool, str, Dict]:
        """
        🔍 Master validation function for all trade requests
        Returns: (is_valid, reason, modified_request)
        """
        logger.info(f"🔍 Validating trade request: {trade_request.get('instrument', 'Unknown')}")
        
        try:
            # Extract trade parameters
            pair = trade_request.get('instrument', '')
            units = abs(int(trade_request.get('units', 0)))
            is_buy = int(trade_request.get('units', 0)) > 0
            entry_price = float(trade_request.get('price', 0))
            
            # Get SL and TP from order details
            stop_loss = self._extract_stop_loss(trade_request)
            take_profit = self._extract_take_profit(trade_request)
            
            if not stop_loss or not take_profit:
                return False, "❌ Missing stop loss or take profit", trade_request
            
            # 1. Validate reward-to-risk ratio
            is_valid_rr, rr_reason = self._validate_reward_risk(
                entry_price, stop_loss, take_profit, is_buy
            )
            if not is_valid_rr:
                return False, f"❌ R/R: {rr_reason}", trade_request
            
            # 2. Check JPY pair conflicts
            if not self.growth_engine.check_jpy_conflict(pair):
                return False, "❌ JPY pair conflict detected", trade_request
            
            # 3. Validate position size
            signal_confidence = trade_request.get('confidence', 0.7)
            volatility = trade_request.get('volatility', 0.001)
            recent_pnl = self._get_recent_pnl()
            
            optimal_size = self.growth_engine.calculate_smart_position_size(
                pair, signal_confidence, volatility, recent_pnl
            )
            
            # 4. Check if size adjustment needed
            size_adjusted = False
            if abs(units - optimal_size) > optimal_size * 0.1:  # 10% difference
                trade_request['units'] = optimal_size if is_buy else -optimal_size
                size_adjusted = True
                logger.info(f"📊 Position size adjusted: {units} → {optimal_size}")
            
            # 5. Confidence threshold check
            if signal_confidence < self.validation_rules['min_confidence_threshold']:
                return False, f"❌ Low confidence: {signal_confidence:.2f}", trade_request
            
            # 6. Spread check
            spread = trade_request.get('spread', 0)
            if spread > self.validation_rules['max_spread_threshold']:
                return False, f"❌ High spread: {spread:.5f}", trade_request
            
            # 7. Update trade request with growth mode enhancements
            enhanced_request = self._enhance_trade_request(trade_request)
            
            validation_summary = f"✅ Trade validated: {pair} | Size: {optimal_size} | R/R: {self._calculate_rr_ratio(entry_price, stop_loss, take_profit, is_buy):.2f}"
            if size_adjusted:
                validation_summary += " | SIZE_ADJUSTED"
                
            return True, validation_summary, enhanced_request
            
        except Exception as e:
            logger.error(f"❌ Validation error: {e}")
            return False, f"❌ Validation error: {str(e)}", trade_request

    def _validate_reward_risk(self, entry: float, sl: float, tp: float, is_buy: bool) -> Tuple[bool, str]:
        """Validate reward-to-risk ratio"""
        return self.growth_engine.validate_reward_risk_ratio(entry, sl, tp, is_buy), "Good R/R ratio"

    def _calculate_rr_ratio(self, entry: float, sl: float, tp: float, is_buy: bool) -> float:
        """Calculate R/R ratio"""
        if is_buy:
            risk = entry - sl
            reward = tp - entry
        else:
            risk = sl - entry
            reward = entry - tp
            
        return reward / risk if risk > 0 else 0

    def _extract_stop_loss(self, trade_request: Dict) -> Optional[float]:
        """Extract stop loss from trade request"""
        # Check various possible locations for SL
        sl_locations = [
            'stopLossOnFill.price',
            'stopLoss.price',
            'stop_loss',
            'sl'
        ]
        
        for location in sl_locations:
            if '.' in location:
                parts = location.split('.')
                value = trade_request
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        value = None
                        break
                if value is not None:
                    return float(value)
            else:
                if location in trade_request:
                    return float(trade_request[location])
        
        return None

    def _extract_take_profit(self, trade_request: Dict) -> Optional[float]:
        """Extract take profit from trade request"""
        # Check various possible locations for TP
        tp_locations = [
            'takeProfitOnFill.price',
            'takeProfit.price',
            'take_profit',
            'tp'
        ]
        
        for location in tp_locations:
            if '.' in location:
                parts = location.split('.')
                value = trade_request
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        value = None
                        break
                if value is not None:
                    return float(value)
            else:
                if location in trade_request:
                    return float(trade_request[location])
        
        return None

    def _get_recent_pnl(self) -> float:
        """Get recent P&L for position sizing"""
        try:
            pnl_file = '/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/data/daily_pnl.json'
            if os.path.exists(pnl_file):
                with open(pnl_file, 'r') as f:
                    pnl_data = json.load(f)
                    return pnl_data.get('current_daily_pnl', 0.0)
        except Exception as e:
            logger.error(f"❌ Error getting recent P&L: {e}")
        
        return 0.0

    def _enhance_trade_request(self, trade_request: Dict) -> Dict:
        """Enhance trade request with growth mode metadata"""
        enhanced = trade_request.copy()
        
        # Add growth mode metadata
        enhanced['growth_mode'] = {
            'validated': True,
            'validation_time': datetime.datetime.now().isoformat(),
            'constitutional_pin': self.growth_engine.constitutional_pin,
            'target_daily_profit': self.growth_engine.target_daily_profit,
            'confidence_threshold': self.growth_engine.confidence_threshold
        }
        
        # Add tracking identifiers
        enhanced['tracking'] = {
            'growth_engine_version': '1.0',
            'validation_source': 'OANDA_POSITION_VALIDATOR',
            'entry_time': datetime.datetime.now().isoformat()
        }
        
        return enhanced

    def create_validation_report(self, validation_results: List[Tuple]) -> Dict:
        """Create a validation report for multiple trades"""
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'total_validations': len(validation_results),
            'passed': sum(1 for result in validation_results if result[0]),
            'failed': sum(1 for result in validation_results if not result[0]),
            'details': []
        }
        
        for is_valid, reason, request in validation_results:
            report['details'].append({
                'instrument': request.get('instrument', 'Unknown'),
                'valid': is_valid,
                'reason': reason,
                'units': request.get('units', 0)
            })
        
        return report

def validate_single_trade(trade_json: str) -> Dict:
    """
    🎯 Standalone function to validate a single trade
    Usage: python3 oanda_position_validator.py '{"instrument": "EUR_USD", "units": 1000, ...}'
    """
    try:
        trade_request = json.loads(trade_json)
        validator = OandaPositionValidator()
        
        is_valid, reason, enhanced_request = validator.validate_trade_request(trade_request)
        
        result = {
            'valid': is_valid,
            'reason': reason,
            'original_request': trade_request,
            'enhanced_request': enhanced_request if is_valid else None,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        return {
            'valid': False,
            'reason': f"❌ Validation error: {str(e)}",
            'original_request': trade_json,
            'enhanced_request': None,
            'timestamp': datetime.datetime.now().isoformat()
        }

def main():
    if len(sys.argv) > 1:
        # Validate trade from command line
        trade_json = sys.argv[1]
        result = validate_single_trade(trade_json)
        print(json.dumps(result, indent=2))
        return
    
    print("🎯 OANDA POSITION VALIDATOR")
    print("=" * 40)
    print("Constitutional PIN: 841921")
    print("Integration: Smart Profit Growth Mode")
    print()
    
        "instrument": "EUR_USD",
        "units": 1000,
        "price": 1.1000,
        "stopLossOnFill": {"price": 1.0950},
        "takeProfitOnFill": {"price": 1.1075},
        "confidence": 0.85,
        "volatility": 0.0012,
        "spread": 0.0002
    }
    
    print("🧪 Testing with sample trade:")
    print()
    
    validator = OandaPositionValidator()
    
    print(f"✅ Validation Result: {is_valid}")
    print(f"📋 Reason: {reason}")
    
    if is_valid:
        print("\n🎯 Enhanced Trade Request:")
        print(json.dumps(enhanced, indent=2))

if __name__ == "__main__":
    main()
