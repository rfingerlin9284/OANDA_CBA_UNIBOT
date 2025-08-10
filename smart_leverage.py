def compute_leverage(confidence, volatility):
    if confidence > 0.9 and volatility < 0.02:
        return 5
    elif confidence > 0.85:
        return 3
    elif confidence > 0.75:
        return 2
    else:
        return 1
