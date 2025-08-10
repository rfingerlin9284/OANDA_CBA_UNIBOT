import json

def fuse_orderbooks(oanda_orderbook, coinbase_orderbook):
    def normalize(book):
        total_volume = sum(abs(x['size']) for x in book)
        return [x['size']/total_volume if total_volume else 0 for x in book]

    try:
        oanda_normalized = normalize(oanda_orderbook)
        coinbase_normalized = normalize(coinbase_orderbook)
    except Exception as e:
        print(f"[ERROR] Normalizing orderbooks: {e}")
        return [0.0] * 5  # fallback

    fused = []
    for i in range(min(len(oanda_normalized), len(coinbase_normalized), 5)):
        fused.append((oanda_normalized[i] + coinbase_normalized[i]) / 2)
    return fused
