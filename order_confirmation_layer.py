def confirm_order(order):
    return order.get('oco') and order.get('stop_loss') and order.get('take_profit')
