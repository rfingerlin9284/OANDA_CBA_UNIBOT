import time
import os

def dynamic_trade_size(confidence: float, equity: float) -> int:
    """
    Confidence-based position amplifier for $400/day profit targeting
    Uses dynamic lot sizing based on ML confidence scores
    """
    base_size = equity * 0.015  # 1.5% base risk
    
    if confidence > 0.9:
        multiplier = 3.0  # High confidence = 3x size
    elif confidence > 0.8:
        multiplier = 2.0  # Good confidence = 2x size
    elif confidence > 0.7:
        multiplier = 1.5  # Decent confidence = 1.5x size
    else:
        multiplier = 1.0  # Low confidence = base size
    
    # Target 75 pips/day across 2-3 trades
    daily_target_units = int(equity / 400 * 75)  # Scale for $400/day target
    
    final_size = min(int(base_size * multiplier), daily_target_units)
    
    print(f"📊 SMART SCALING: Confidence={confidence:.1%} | Multiplier={multiplier}x | Units={final_size}")
    return final_size

def cooldown_timer(last_trade_time, cooldown_secs=1800):
    """30-minute cooldown between trades on same pair"""
    return time.time() - last_trade_time > cooldown_secs

def should_reenter_trade(prev_result: str, current_confidence: float):
    """Re-entry logic for winning trades with high confidence"""
    return prev_result == 'WIN' and current_confidence > 0.85

def daily_profit_tracker():
    """Track progress toward $400/day target"""
    log_file = f"{os.path.dirname(__file__)}/logs/daily_profit.log"
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            today_profit = sum(float(line.split(',')[1]) for line in lines if line.startswith(time.strftime("%Y-%m-%d")))
            return today_profit
    except:
        return 0.0

def profit_target_reached():
    """Check if $400 daily target is reached"""
    return daily_profit_tracker() >= 400.0
