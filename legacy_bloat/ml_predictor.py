import pickle, pandas as pd

def load_model(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def run_prediction(model, features):
    X = pd.DataFrame([features])
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    return pred, max(proba)
