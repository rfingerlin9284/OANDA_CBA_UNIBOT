import time, logging

def assess_and_exit(trades, pnl_data, fees):
    for trade in trades:
        if trade['unrealized_pl'] > fees * 1.2 and trade['confidence'] > 0.7:
            logging.info(f"✅ Harvesting trade: {trade['id']}")
            # Close trade logic here

def reallocate_capital(allocations, performance_metrics):
    for bot, perf in performance_metrics.items():
        if perf['roi'] > 0.03:
            allocations[bot] *= 1.1
        elif perf['roi'] < 0:
            allocations[bot] *= 0.9
    return allocations
