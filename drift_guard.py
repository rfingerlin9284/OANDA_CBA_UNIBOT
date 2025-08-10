PAIR_HISTORY_LIMIT = 12
MAX_PAIR_OCCURRENCE = 3
pair_history = []

def is_pair_overused(pair):
    global pair_history
    pair_history.append(pair)
    if len(pair_history) > PAIR_HISTORY_LIMIT:
        pair_history = pair_history[-PAIR_HISTORY_LIMIT:]
    return pair_history.count(pair) > MAX_PAIR_OCCURRENCE
