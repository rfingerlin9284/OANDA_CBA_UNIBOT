LIVE_TRADING_ENABLED = False
SANDBOX_BACKTEST_MODE = True
#!/usr/bin/env python3

import os, time, logging
from strategy_voter import vote_on_strategies
from trade_harvest_manager import assess_and_exit
from order_confirmation_layer import confirm_order
from smart_leverage import compute_leverage
from profit_gating import should_take_profit
from budget_allocator import reallocate_strategy_budget
from trade_filter import is_trade_worthwhile
from trade_auditor import audit_trades
from oco_enforcer import validate_oco
from cobra_strike import cobra_strike
from oco_overlay_validator import check_oco_status
from cobra_overlay_logger import cobra_strike as cobra_overlay
from profit_gating_overlay import should_take_profit as profit_overlay

# 🔐 Live Credentials (Hardcoded)
API_KEY = "2636c881-b44e-4263-b05d-fb10a5ad1836"
API_SECRET = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
API_URL = "https://api.cdp.coinbase.com"

# 🔁 Trading Loop
def main():
    logging.basicConfig(filename="cb_bot.log", level=logging.INFO)
    logging.info("🚀 Coinbase Bot Launching Live with Tier 2 Enhancements...")

    # Initialize strategy stats for budget allocation
    strategy_stats = {
        "model1": {"win_rate": 0.8, "alloc": 1.0},
        "model2": {"win_rate": 0.75, "alloc": 1.0},
        "model3": {"win_rate": 0.6, "alloc": 1.0}
    }

    while True:
        try:
            # TODO: Fetch account, positions, signals, and predictions
            # Dummy predictions (replace with real ML logic)
            predictions = {"model1": "buy", "model2": "buy", "model3": "sell"}
            confidences = {"model1": 0.9, "model2": 0.8, "model3": 0.4}

            # 🐍 COBRA STRIKE MODE - Multi-model consensus
            cobra_overlay(confidences)  # Overlay logging
            if cobra_strike(confidences):
                logging.info("🐍 COBRA STRIKE ACTIVATED - High confidence consensus!")
                leverage_multiplier = 1.5  # Boost leverage for cobra strikes
            else:
                leverage_multiplier = 1.0

            final_vote = vote_on_strategies(predictions, confidences)
            logging.info(f"📊 Strategy voted: {final_vote.upper()}")

            # 💰 Smart Leverage Calculation
            avg_confidence = sum(confidences.values()) / len(confidences)
            volatility = 0.015  # TODO: Replace with real volatility calculation
            base_leverage = compute_leverage(avg_confidence, volatility)
            final_leverage = base_leverage * leverage_multiplier
            
            logging.info(f"⚡ Leverage: {final_leverage}x (base: {base_leverage}x, multiplier: {leverage_multiplier}x)")

            # 💸 Fee Filter Check
            entry_price = 50000  # TODO: Get real market price
            target_profit = 150  # TODO: Calculate based on strategy
            fees = 25  # TODO: Calculate real fees
            
            if not is_trade_worthwhile(entry_price, target_profit, fees):
                logging.warning("💸 Trade filtered out - insufficient profit vs fees")
                continue

            order = {
                "direction": final_vote,
                "oco": True,
                "stop_loss": True,
                "take_profit": True,
                "leverage": final_leverage
            }

            # 🛡️ Enhanced OCO Validation
            if not validate_oco(order):
                logging.error("⚠️ OCO validation failed - canceling trade")
                continue

            # 🔍 OCO Overlay Check
            oco_alerts = check_oco_status([order])
            for alert in oco_alerts:
                logging.info(f"[OCO OVERLAY] {alert}")

            if confirm_order(order):
                logging.info("🟢 Order passed all filters. Placing live order...")
                # PLACE ORDER LOGIC HERE
                
                # 💰 Profit Gating Overlay for future reference
                dummy_trade = {"unrealized_pl": 75, "fees": 25}
                profit_overlay(dummy_trade)  # This will log the profit gating status
                
            else:
                logging.warning("⚠️ Order missing protection layers!")

            # 📊 Budget Reallocation (daily)
            strategy_stats = reallocate_strategy_budget(strategy_stats)
            logging.info(f"💼 Strategy allocations updated: {strategy_stats}")

            # Evaluate existing trades and exit logic
            assess_and_exit([], {}, 0.1)

        except Exception as e:
            logging.error(f"❌ Runtime Error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
