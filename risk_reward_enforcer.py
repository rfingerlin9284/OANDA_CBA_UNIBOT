#!/usr/bin/env python3
"""Risk/Reward Enforcer - Blocks Bad R/R Trades"""

class RiskRewardEnforcer:
    def __init__(self):
        self.min_risk_reward = 1.5  # Minimum 1.5:1 R/R ratio
        self.ideal_risk_reward = 2.0  # Target 2:1 R/R ratio
        
    def validate_risk_reward(self, entry_price, stop_loss, take_profit, side):
        """
        ⚖️ R/R ENFORCEMENT: Block trades with bad risk/reward math
        Fixes: SL=195.200, TP=195.800, Entry=195.429 (risking 200 pips for 37)
        """
        try:
            if side.upper() == 'BUY':
                risk = abs(entry_price - stop_loss)
                reward = abs(take_profit - entry_price)
            else:  # SELL
                risk = abs(stop_loss - entry_price)
                reward = abs(entry_price - take_profit)
            
            if risk <= 0:
                return False, "Invalid stop loss"
            
            risk_reward_ratio = reward / risk
            
            print(f"⚖️ RISK/REWARD ANALYSIS:")
            print(f"   Entry: {entry_price:.5f}")
            print(f"   Stop Loss: {stop_loss:.5f}")
            print(f"   Take Profit: {take_profit:.5f}")
            print(f"   Risk: {risk:.5f} ({(risk/entry_price)*100:.2f}%)")
            print(f"   Reward: {reward:.5f} ({(reward/entry_price)*100:.2f}%)")
            print(f"   R/R Ratio: {risk_reward_ratio:.2f}:1")
            
            if risk_reward_ratio >= self.ideal_risk_reward:
                print(f"✅ EXCELLENT R/R: {risk_reward_ratio:.2f}:1 (target: {self.ideal_risk_reward}:1)")
                return True, "Excellent risk/reward"
            elif risk_reward_ratio >= self.min_risk_reward:
                print(f"✅ ACCEPTABLE R/R: {risk_reward_ratio:.2f}:1 (min: {self.min_risk_reward}:1)")
                return True, "Acceptable risk/reward"
            else:
                print(f"🚫 BAD R/R RATIO: {risk_reward_ratio:.2f}:1 < {self.min_risk_reward}:1 minimum")
                return False, f"Risk/reward too low: {risk_reward_ratio:.2f}:1"
                
        except Exception as e:
            return False, f"R/R calculation error: {e}"

    """Test risk/reward enforcement"""
    enforcer = RiskRewardEnforcer()
    
        # Bad R/R case from your screenshot
        {"entry": 195.429, "sl": 195.200, "tp": 195.800, "side": "BUY"},
        # Good R/R case
        {"entry": 1.1000, "sl": 1.0950, "tp": 1.1100, "side": "BUY"},
        # Excellent R/R case
        {"entry": 1.1000, "sl": 1.0980, "tp": 1.1040, "side": "BUY"}
    ]
    
        print(f"\n🧪 TEST CASE {i}:")
        valid, reason = enforcer.validate_risk_reward(**case)
        print(f"Result: {'PASS' if valid else 'FAIL'} - {reason}")

if __name__ == "__main__":
