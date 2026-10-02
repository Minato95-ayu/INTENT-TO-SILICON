# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

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


class NeuralNet:
    def __init__(self, layers, lr=0.01):
        self.layers = layers
        self.lr = lr
        self.weights = []
        self.biases = []
        # Initialize random weights
        for i in range(len(layers)-1):
            w = [[random.uniform(-1, 1) for _ in range(layers[i+1])] for _ in range(layers[i])]
            b = [0.0 for _ in range(layers[i+1])]
            self.weights.append(w)
            self.biases.append(b)

    def _sigmoid(self, x):
        return 1.0 / (1.0 + math.exp(-x))

    def _sigmoid_deriv(self, x):
        return x * (1.0 - x)

    def forward(self, X):
        self.activations = [X]
        curr = X
        for w, b in zip(self.weights, self.biases):
            next_act = []
            for j in range(len(w[0])):
                s = sum(curr[k] * w[k][j] for k in range(len(w))) + b[j]
                next_act.append(self._sigmoid(s))
            curr = next_act
            self.activations.append(curr)
        return curr

    def train_step(self, X, y):
        pred = self.forward(X)
        
        # Backprop
        errors = [y[i] - pred[i] for i in range(len(y))]
        deltas = [errors[i] * self._sigmoid_deriv(pred[i]) for i in range(len(pred))]
        
        for layer in range(len(self.weights)-1, -1, -1):
            prev_act = self.activations[layer]
            next_deltas = [0.0 for _ in range(len(prev_act))]
            
            for j in range(len(self.weights[layer][0])):
                # Update bias
                self.biases[layer][j] += self.lr * deltas[j]
                # Update weights and calculate next delta
                for k in range(len(prev_act)):
                    next_deltas[k] += deltas[j] * self.weights[layer][k][j]
                    self.weights[layer][k][j] += self.lr * deltas[j] * prev_act[k]
                    
            deltas = [next_deltas[k] * self._sigmoid_deriv(prev_act[k]) for k in range(len(prev_act))]

def ml_nn_create(layers: list, lr: float = 0.01) -> int:
    MLState._model_id_counter += 1
    model_id = MLState._model_id_counter
    MLState._models[model_id] = {"type": "nn", "model": NeuralNet(layers, lr)}
    return model_id

def ml_nn_train(model_id: int, X: list, y: list, epochs: int = 100):
    model = MLState._models.get(model_id)
    if not model or model["type"] != "nn":
        return
    nn = model["model"]
    for _ in range(epochs):
        for i in range(len(X)):
            pt_x = X[i] if isinstance(X[i], (list, tuple)) else [X[i]]
            pt_y = y[i] if isinstance(y[i], (list, tuple)) else [y[i]]
            nn.train_step(pt_x, pt_y)

def ml_nn_predict(model_id: int, X: list) -> list:
    model = MLState._models.get(model_id)
    if not model or model["type"] != "nn":
        return []
    nn = model["model"]
    preds = []
    for point in X:
        pt = point if isinstance(point, (list, tuple)) else [point]
        preds.append(nn.forward(pt))
    return preds

from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.list import ListValue
from ...values.map import MapValue

def py_to_aayu(py_val, vm):
    if isinstance(py_val, (int, float)): return NumberValue(float(py_val))
    if isinstance(py_val, list):
        l = [py_to_aayu(x, vm) for x in py_val]
        obj = vm.heap.allocate("list", l)
        return ListValue(obj, vm.heap)
    return NumberValue(0.0)

def aayu_to_py(val):
    if hasattr(val, "to_python"): return val.to_python()
    return val

def register_ml_lib(registry: StdLibRegistry):
    def fn_kmeans_fit(args, vm):
        try:
            data = aayu_to_py(args[0])
            k = int(aayu_to_py(args[1])) if len(args) > 1 else 3
            max_iters = int(aayu_to_py(args[2])) if len(args) > 2 else 100
            model_id = ml_kmeans_fit(data, k, max_iters)
            return NumberValue(model_id)
        except Exception:
            return NumberValue(-1)

    def fn_kmeans_predict(args, vm):
        try:
            model_id = int(aayu_to_py(args[0]))
            point = aayu_to_py(args[1])
            cluster = ml_kmeans_predict(model_id, point)
            return NumberValue(cluster)
        except Exception:
            return NumberValue(-1)
            
    def fn_linear_regression_fit(args, vm):
        try:
            X = aayu_to_py(args[0])
            y = aayu_to_py(args[1])
            model_id = ml_linear_regression_fit(X, y)
            return NumberValue(model_id)
        except Exception:
            return NumberValue(-1)
            
    def fn_linear_regression_predict(args, vm):
        try:
            model_id = int(aayu_to_py(args[0]))
            X = aayu_to_py(args[1])
            predictions = ml_linear_regression_predict(model_id, X)
            return py_to_aayu(predictions, vm)
        except Exception:
            return py_to_aayu([], vm)

    registry.register("ml::kmeans_fit", fn_kmeans_fit)
    registry.register("ml::kmeans_predict", fn_kmeans_predict)
    registry.register("ml::linear_regression_fit", fn_linear_regression_fit)
    registry.register("ml::linear_regression_predict", fn_linear_regression_predict)
