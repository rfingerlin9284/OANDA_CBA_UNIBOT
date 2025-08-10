import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
X = df[["RSI", "FVG", "VolumeDelta", "Bias", "PriceChange", "FVGWidth", "IsBreakout", "OrderBookPressure"]]
y = df["Label"]
model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X, y)
joblib.dump(model, "light_heavy_model.pkl")
print("[✅] light_heavy_model.pkl created.")
