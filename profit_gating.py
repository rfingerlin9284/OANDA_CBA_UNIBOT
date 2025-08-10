def should_take_profit(trade):
    if trade['unrealized_pl'] >= trade['fees'] * 3:
        return True
    return False
