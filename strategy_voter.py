def vote_on_strategies(predictions, confidence_scores):
    votes = {k: 0 for k in predictions}
    for model, pred in predictions.items():
        if confidence_scores[model] > 0.75:
            votes[pred] += 1
    return max(votes, key=votes.get)
