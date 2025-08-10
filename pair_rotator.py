import random, time
ROTATION_INTERVAL = 3600  # Rotate every 1 hour
CURRENCY_POOLS = {
    'forex': ['EUR_USD','USD_JPY','GBP_USD','USD_CHF','AUD_USD','USD_CAD','NZD_USD','EUR_GBP','GBP_JPY','EUR_JPY','CHF_JPY','AUD_JPY'],
    'crypto': ['BTC-USD','ETH-USD','SOL-USD','XRP-USD','DOGE-USD','AVAX-USD','ADA-USD','MATIC-USD','LINK-USD','UNI-USD','DOT-USD','LTC-USD']
}
def rotate_pairs(current_mode='forex'):
    pairs = CURRENCY_POOLS.get(current_mode, [])
    return random.sample(pairs, k=4)  # Pick 4 random active instruments
