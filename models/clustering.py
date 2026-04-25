from sklearn.cluster import KMeans

def run_clustering(data):
    features = data[["rent","food","entertainment","shopping"]]
    kmeans = KMeans(n_clusters=3, random_state=42)
    data["cluster"] = kmeans.fit_predict(features)
    return data