def cobra_strike(model_predictions, threshold=0.85):
    strong = [k for k,v in model_predictions.items() if v >= threshold]
    if len(strong) >= 2:
        print(f"[COBRA STRIKE] 🎯 Models agree: {strong}")
        return True
    print(f"[COBRA STRIKE] ⚠️ Models disagree: {model_predictions}")
    return False
