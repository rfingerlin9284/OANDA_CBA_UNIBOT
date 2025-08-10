import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from feature_list import FEATURE_COLUMNS

def load_csvs(path):
    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".csv")]
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

def train_model(data, model_type):
    data = data.dropna(subset=FEATURE_COLUMNS + ['Label'])
    X = data[FEATURE_COLUMNS]
    y = data['Label']
    if model_type == "light":
        return RandomForestClassifier(n_estimators=120).fit(X, y)
    return XGBClassifier(n_estimators=250, max_depth=8).fit(X, y)

df = load_csvs("data/coinbase")
light = train_model(df, "light")
heavy = train_model(df, "heavy")
joblib.dump(light, "light_heavy_model.pkl")
print("[✅] Retrain complete.")
