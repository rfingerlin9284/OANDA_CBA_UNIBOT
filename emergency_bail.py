WIN_RATE_THRESHOLD = 0.35
WIN_RATE_WINDOW = 12

trade_results = []
bailout_triggered = False

def record_trade_result(win: bool):
    global trade_results, bailout_triggered
    trade_results.append(win)
    if len(trade_results) > WIN_RATE_WINDOW:
        trade_results = trade_results[-WIN_RATE_WINDOW:]
    win_rate = sum(trade_results) / len(trade_results) if trade_results else 1.0
    if win_rate < WIN_RATE_THRESHOLD and len(trade_results) == WIN_RATE_WINDOW:
        bailout_triggered = True
        print("⛔ EMERGENCY BAILOUT TRIGGERED: Win rate below threshold. Trading halted.")

def is_bailout_triggered():
    return bailout_triggered

def reset_bailout():
    global bailout_triggered, trade_results
    bailout_triggered = False
    trade_results = []
    print("✅ Emergency bailout reset. Trading re-enabled.")
