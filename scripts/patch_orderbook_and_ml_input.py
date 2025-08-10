import json
import pandas as pd
import numpy as np

def safe_get_buckets(orderbook):
    """Safely extract buckets from OANDA orderbook response"""
    try:
        # Handle both direct buckets and nested orderBook.buckets
        if "buckets" in orderbook:
            return orderbook["buckets"]
        elif "orderBook" in orderbook and "buckets" in orderbook["orderBook"]:
            return orderbook["orderBook"]["buckets"]
        else:
            return []
    except (KeyError, TypeError):
        return []

def predict_with_names(model, features_dict):
    """Predict using DataFrame with proper feature names"""
    df = pd.DataFrame([features_dict])
    predictions = model.predict(df)
    probabilities = model.predict_proba(df)
    return predictions, probabilities

def safe_json_dump(data, path):
    """JSON dump with numpy type conversion"""
    def convert_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bool):
            return bool(obj)
        return obj
    
    # Convert all values recursively
    converted_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            converted_data[k] = {k2: convert_types(v2) for k2, v2 in v.items()}
        else:
            converted_data[k] = convert_types(v)
    
    with open(path, "w") as f:
        json.dump(converted_data, f, indent=2)
