import os
import pandas as pd
import numpy as np

DATA_DIR = "data/oanda"
RESULTS_FILE = "pnl_summary.csv"

# Strategy parameters
STOP_LOSS = 0.003  # 0.3%
TAKE_PROFIT = 0.006  # 0.6%
MAX_HOLD = 12  # max bars held (e.g. 1 hr for 5m data)

summary = []

for fname in os.listdir(DATA_DIR):
    if not fname.endswith("_features.csv"):
        continue

    pair = fname.replace("_features.csv", "")
    df = pd.read_csv(os.path.join(DATA_DIR, fname))

    # Sanity check
    if not all(col in df.columns for col in ['open', 'high', 'low', 'close', 'rsi', 'ema_cross', 'fvg_strength']):
        print(f"❌ Missing columns in {fname}")
        continue

    trades = []
    in_trade = False
    entry_price = 0
    entry_index = 0
    direction = None

    for i in range(len(df)):
        if not in_trade:
            if df.loc[i, 'rsi'] < 30 and df.loc[i, 'ema_cross'] == 1 and df.loc[i, 'fvg_strength'] > 0.5:
                # Enter long
                in_trade = True
                entry_price = df.loc[i, 'close']
                entry_index = i
                direction = "long"
        else:
            current_price = df.loc[i, 'close']
            high = df.loc[i, 'high']
            low = df.loc[i, 'low']

            # SL/TP logic
            sl_hit = (low <= entry_price * (1 - STOP_LOSS))
            tp_hit = (high >= entry_price * (1 + TAKE_PROFIT))
            max_bars = (i - entry_index) >= MAX_HOLD

            exit_price = current_price
            exited = False

            if tp_hit:
                exit_price = entry_price * (1 + TAKE_PROFIT)
                exited = True
            elif sl_hit:
                exit_price = entry_price * (1 - STOP_LOSS)
                exited = True
            elif max_bars:
                exited = True

            if exited:
                profit = exit_price - entry_price
                pct = profit / entry_price
                trades.append(pct)
                in_trade = False

    # Summary
    wins = [t for t in trades if t > 0]
    losses = [t for t in trades if t <= 0]
    net = sum(trades)
    winrate = len(wins) / len(trades) if trades else 0
    drawdown = min(np.cumsum(trades)) if trades else 0

    summary.append({
        'pair': pair,
        'trades': len(trades),
        'wins': len(wins),
        'losses': len(losses),
        'winrate': round(winrate * 100, 2),
        'net_pnl_%': round(net * 100, 2),
        'max_drawdown_%': round(drawdown * 100, 2)
    })

# Save results
pd.DataFrame(summary).to_csv(RESULTS_FILE, index=False)
print(f"\n✅ PnL Simulation Complete! Summary saved to: {RESULTS_FILE}")
