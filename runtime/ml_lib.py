"""
=============================================================================
FILE: ml_lib.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import statistics

def ml_mean(data):
    if not isinstance(data, list) or not data:
        return 0.0
    return statistics.mean(data)

def ml_median(data):
    if not isinstance(data, list) or not data:
        return 0.0
    return statistics.median(data)

def ml_std(data):
    if not isinstance(data, list) or len(data) < 2:
        return 0.0
    return statistics.stdev(data)

def ml_matrix_add(mat_a, mat_b):
    # mat_a and mat_b should be lists of lists
    if not mat_a or not mat_b:
        return []
    if len(mat_a) != len(mat_b) or len(mat_a[0]) != len(mat_b[0]):
        raise ValueError("Matrix dimensions must match for addition.")
        
    result = []
    for i in range(len(mat_a)):
        row = []
        for j in range(len(mat_a[0])):
            row.append(mat_a[i][j] + mat_b[i][j])
        result.append(row)
    return result

def ml_matrix_multiply(mat_a, mat_b):
    if not mat_a or not mat_b:
        return []
    rows_a = len(mat_a)
    cols_a = len(mat_a[0])
    rows_b = len(mat_b)
    cols_b = len(mat_b[0])
    
    if cols_a != rows_b:
        raise ValueError(f"Cannot multiply matrix: {rows_a}x{cols_a} with {rows_b}x{cols_b}")
        
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += mat_a[i][k] * mat_b[k][j]
    return result

def ml_linear_regression(X, y):
    # Simple linear regression for 1D arrays: y = mx + c
    # Returns [m, c]
    if len(X) != len(y) or len(X) < 2:
        raise ValueError("X and y must be lists of the same length (>1).")
        
    n = len(X)
    mean_x = statistics.mean(X)
    mean_y = statistics.mean(y)
    
    numer = sum((X[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denom = sum((X[i] - mean_x) ** 2 for i in range(n))
    
    if denom == 0:
        return [0.0, mean_y]
        
    m = numer / denom
    c = mean_y - (m * mean_x)
    return [m, c]

# Module registry
ML_MODULE = {
    "mean": ml_mean,
    "median": ml_median,
    "std": ml_std,
    "matrix_add": ml_matrix_add,
    "matrix_multiply": ml_matrix_multiply,
    "linear_regression": ml_linear_regression
}
