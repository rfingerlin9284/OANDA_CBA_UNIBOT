# === AUTO-INJECTED BY inject_full_telemetry_logger.sh ===
# === TELEMETRY LOGGER START ===
import json, os
from datetime import datetime

def log_telemetry(prediction, confidence, model_name):
    """Thread-safe telemetry logging for ML predictions"""
    try:
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "prediction": str(prediction),
            "confidence": round(float(confidence), 4),
            "model": model_name,
            "constitutional_pin": "841921"
        }
        with open("logs/ml_predictions.log", "a") as f:
            f.write("ML DECISION: " + json.dumps(payload) + "\n")
    except Exception as e:
        print(f"[⚠️] Telemetry logging failed: {e}")
# === TELEMETRY LOGGER END ===

#!/usr/bin/env python3
# 🧠 ML Decision Filter - Fee-aware, confidence-adjusted predictor
# Filters bad trades before execution to protect capital

import logging
from datetime import datetime
import json

class MLDecisionFilter:
    def __init__(self, confidence_threshold=0.72, min_net_return=0.003):
        self.confidence_threshold = confidence_threshold
        self.min_net_return = min_net_return
        self.rejection_log = []
        
    def approve_trade(self, prediction, fee_estimate, symbol="UNKNOWN"):
        """
        Fee-aware trade approval with confidence filtering
        Returns: (approved: bool, reason: str, adjusted_prediction: dict)
        """
        try:
            expected_return = prediction.get('expected_return', 0)
            confidence = prediction.get('confidence', 0)
            
            # Calculate net return after fees
            projected_net = expected_return - fee_estimate
            
            # Multi-layer approval logic
            if confidence < self.confidence_threshold:
                reason = f"❌ LOW CONFIDENCE: {confidence:.2f} < {self.confidence_threshold}"
                self.log_rejection(symbol, reason, prediction, fee_estimate)
                return False, reason, prediction
                
            if projected_net <= self.min_net_return:
                reason = f"❌ INSUFFICIENT NET: {projected_net:.4f} ≤ {self.min_net_return} after fees"
                self.log_rejection(symbol, reason, prediction, fee_estimate)
                return False, reason, prediction
                
            # Fee ratio check - reject if fees > 30% of expected return
            if fee_estimate > (expected_return * 0.3):
                reason = f"❌ HIGH FEE RATIO: {(fee_estimate/expected_return)*100:.1f}% of expected return"
                self.log_rejection(symbol, reason, prediction, fee_estimate)
                return False, reason, prediction
            
            # Enhanced prediction with fee adjustment
            adjusted_prediction = prediction.copy()
            adjusted_prediction['net_return'] = projected_net
            adjusted_prediction['fee_ratio'] = fee_estimate / expected_return if expected_return > 0 else 1
            adjusted_prediction['approval_score'] = confidence * projected_net
            
            reason = f"✅ APPROVED: net={projected_net:.4f}, conf={confidence:.2f}, fee_ratio={adjusted_prediction['fee_ratio']:.1%}"
            self.log_approval(symbol, reason, adjusted_prediction)
            
            return True, reason, adjusted_prediction
            
        except Exception as e:
            reason = f"❌ FILTER ERROR: {str(e)}"
            self.log_rejection(symbol, reason, prediction, fee_estimate)
            return False, reason, prediction
    
    def log_rejection(self, symbol, reason, prediction, fee_estimate):
        """Log rejected trades for analysis"""
        rejection = {
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol,
            'reason': reason,
            'prediction': prediction,
            'fee_estimate': fee_estimate
        }
        self.rejection_log.append(rejection)
        
        # Keep only last 100 rejections
        if len(self.rejection_log) > 100:
            self.rejection_log = self.rejection_log[-100:]
            
        logging.info(f"TRADE REJECTED: {symbol} - {reason}")
    
    def log_approval(self, symbol, reason, prediction):
        """Log approved trades"""
        logging.info(f"TRADE APPROVED: {symbol} - {reason}")
    
    def get_rejection_stats(self):
        """Get rejection statistics for optimization"""
        if not self.rejection_log:
            return {"total_rejections": 0}
            
        recent_rejections = self.rejection_log[-20:]  # Last 20
        reasons = {}
        
        for rejection in recent_rejections:
            reason_type = rejection['reason'].split(':')[0]
            reasons[reason_type] = reasons.get(reason_type, 0) + 1
            
        return {
            "total_rejections": len(self.rejection_log),
            "recent_rejections": len(recent_rejections),
            "rejection_reasons": reasons,
            "rejection_rate": len(recent_rejections) / 20 if len(recent_rejections) == 20 else None
        }
