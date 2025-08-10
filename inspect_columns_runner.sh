#!/bin/bash
# 🔍 RUN THIS TO SEE HEADERS IN _features.csv FILES

source ./venv/bin/activate

cat << 'PYEOF' > inspect_csv_columns.py
import os
import pandas as pd

DATA_DIR = "data/oanda"
for filename in os.listdir(DATA_DIR):
    if filename.endswith("_features.csv"):
        path = os.path.join(DATA_DIR, filename)
        try:
            df = pd.read_csv(path, nrows=2)
            print(f"📂 {filename}: {list(df.columns)}")
        except Exception as e:
            print(f"❌ {filename} failed: {e}")
PYEOF

python3 inspect_csv_columns.py
