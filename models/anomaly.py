from sklearn.ensemble import IsolationForest

def detect_anomalies(data):
    features = data[["rent", "food", "entertainment", "shopping"]]

    model = IsolationForest(contamination=0.05, random_state=42)

    data["anomaly"] = model.fit_predict(features)

    return data