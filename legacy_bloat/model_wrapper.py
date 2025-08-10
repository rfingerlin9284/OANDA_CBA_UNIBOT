import joblib
def load_model(path):
    return joblib.load(path)
def predict_confidence(model, X):
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[0][1]
    return model.predict(X)[0]
def load_models():
    light = load_model("light_heavy_model.pkl")
    return light, heavy
