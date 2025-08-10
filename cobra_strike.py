def cobra_strike(model_predictions, threshold=0.85):
    strong_agreement = [m for m, c in model_predictions.items() if c >= threshold]
    return len(strong_agreement) >= 2
