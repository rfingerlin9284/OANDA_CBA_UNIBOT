def audit_trades(trade_history):
    poor_performers = []
    for t in trade_history:
        if t['result'] == 'LOSS' and t['confidence'] > 0.7:
            poor_performers.append(t)
    return poor_performers
