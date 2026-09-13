import math
import random

# AAYU ML Module - Pure Python Implementation (Zero Dependencies)

class MLState:
    _models = {}
    _model_id_counter = 0

def ml_kmeans_fit(data: list, k: int = 3, max_iters: int = 100) -> int:
    """Trains a K-Means model on the given dataset and returns a model ID."""
    if not data or not isinstance(data, list):
        return -1
    
    # Randomly initialize centroids from data
    centroids = random.sample(data, min(k, len(data)))
    
    for _ in range(max_iters):
        clusters = {i: [] for i in range(k)}
        
        # Assign points to nearest centroid
        for point in data:
            if not isinstance(point, (list, tuple)):
                point = [point]
            
            best_i = 0
            best_dist = float('inf')
            for i, c in enumerate(centroids):
                if not isinstance(c, (list, tuple)):
                    c = [c]
                # Euclidean distance
                dist = sum((a - b) ** 2 for a, b in zip(point, c))
                if dist < best_dist:
                    best_dist = dist
                    best_i = i
            clusters[best_i].append(point)
            
        # Update centroids
        new_centroids = []
        for i in range(k):
            if clusters[i]:
                dims = len(clusters[i][0])
                new_c = [sum(pt[d] for pt in clusters[i]) / len(clusters[i]) for d in range(dims)]
                new_centroids.append(new_c)
            else:
                new_centroids.append(centroids[i])
                
        if new_centroids == centroids:
            break
        centroids = new_centroids
        
    MLState._model_id_counter += 1
    model_id = MLState._model_id_counter
    MLState._models[model_id] = {"type": "kmeans", "centroids": centroids, "k": k}
    return model_id

def ml_kmeans_predict(model_id: int, data: list) -> list:
    """Predicts the cluster index for a list of points."""
    model = MLState._models.get(model_id)
    if not model or model["type"] != "kmeans":
        return []
    
    centroids = model["centroids"]
    predictions = []
    
    for point in data:
        if not isinstance(point, (list, tuple)):
            point = [point]
            
        best_i = 0
        best_dist = float('inf')
        for i, c in enumerate(centroids):
            if not isinstance(c, (list, tuple)):
                c = [c]
            dist = sum((a - b) ** 2 for a, b in zip(point, c))
            if dist < best_dist:
                best_dist = dist
                best_i = i
        predictions.append(best_i)
        
    return predictions

def ml_linear_regression_fit(X: list, y: list, lr: float = 0.01, epochs: int = 1000) -> int:
    """Trains a Linear Regression model using Gradient Descent."""
    if not X or not y or len(X) != len(y):
        return -1
    
    dims = len(X[0]) if isinstance(X[0], (list, tuple)) else 1
    weights = [0.0] * dims
    bias = 0.0
    
    for _ in range(epochs):
        for i, point in enumerate(X):
            pt = point if isinstance(point, (list, tuple)) else [point]
            pred = sum(w * x for w, x in zip(weights, pt)) + bias
            error = pred - y[i]
            
            # Gradient descent step
            for d in range(dims):
                weights[d] -= lr * error * pt[d]
            bias -= lr * error
            
    MLState._model_id_counter += 1
    model_id = MLState._model_id_counter
    MLState._models[model_id] = {"type": "linreg", "weights": weights, "bias": bias}
    return model_id

def ml_linear_regression_predict(model_id: int, X: list) -> list:
    """Predicts values using a trained Linear Regression model."""
    model = MLState._models.get(model_id)
    if not model or model["type"] != "linreg":
        return []
    
    weights = model["weights"]
    bias = model["bias"]
    predictions = []
    
    for point in X:
        pt = point if isinstance(point, (list, tuple)) else [point]
        pred = sum(w * x for w, x in zip(weights, pt)) + bias
        predictions.append(pred)
        
    return predictions
