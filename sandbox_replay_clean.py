# Description: Runs historical .csv features through trained ML model
# Output: Logs prediction + confidence per row for quick sanity check

import os
import pandas as pd
import joblib

DATA_DIR = "data/oanda"
FEATURES_USED = ['returns', 'volatility', 'ma_fast', 'ma_slow']

def replay_pair(pair_file, model):
    pair_name = pair_file.replace('_features.csv', '')
    full_path = os.path.join(DATA_DIR, pair_file)

    try:
        df = pd.read_csv(full_path)
        df.dropna(subset=FEATURES_USED, inplace=True)
        X = df[FEATURES_USED]
        preds = model.predict(X)
        probs = model.predict_proba(X)

        print(f"\n🎬 {pair_name} — {len(preds)} predictions")
        for i in range(min(5, len(preds))):
            print(f"  🔹 Row {i+1}: Pred = {preds[i]}, Conf = {max(probs[i]):.2f}")
    except Exception as e:
        print(f"❌ Error processing {pair_file}: {e}")

def main():
    print(f"📦 Loading model: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)

    print(f"📁 Scanning feature files in: {DATA_DIR}")
    for file in os.listdir(DATA_DIR):
        if file.endswith('_features.csv'):
            replay_pair(file, model)

if __name__ == "__main__":
    main()
