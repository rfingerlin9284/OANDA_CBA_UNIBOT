import time

PAIR_COOLDOWN_HOURS = 12
_pair_cooldowns = {}

def is_pair_blocked(pair):
    now = time.time()
    if pair in _pair_cooldowns:
        if now < _pair_cooldowns[pair]:
            return True
        else:
            del _pair_cooldowns[pair]
    return False

def block_pair(pair):
    _pair_cooldowns[pair] = time.time() + PAIR_COOLDOWN_HOURS * 3600

def unblock_pair(pair):
    if pair in _pair_cooldowns:
        del _pair_cooldowns[pair]
