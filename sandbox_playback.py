import os
import pandas as pd
from model_wrapper import load_models, predict_confidence
from strategies import detect_trade_signal
from feature_list import FEATURE_COLUMNS

def liveulate_trading(paths, label):
    print(f"📂 {label} Market\n" + "="*40)
    light, heavy = load_models()
    for file in sorted(paths):
        name = os.path.basename(file).replace(".csv", "")
        try:
            df = pd.read_csv(file).dropna(subset=FEATURE_COLUMNS + ['Label'])
            for i in range(len(df)):
                row = df.iloc[i]
                features = [row[col] for col in FEATURE_COLUMNS]
                conf_light = predict_confidence(light, [features])
                conf_heavy = predict_confidence(heavy, [features])
                signal = detect_trade_signal(row)
                print(f"{name} | {row['Label']} | Light: {conf_light:.2f} | Heavy: {conf_heavy:.2f} | Signal: {signal}")
        except Exception as e:
            print(f"[⚠️] Failed {name}: {e}")

liveulate_trading(
    [os.path.join("data/coinbase", f) for f in os.listdir("data/coinbase") if f.endswith(".csv")],
    "Coinbase"
)
liveulate_trading(
    [os.path.join("data/oanda", f) for f in os.listdir("data/oanda") if f.endswith(".csv")],
    "OANDA"
)
