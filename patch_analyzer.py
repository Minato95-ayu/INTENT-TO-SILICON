import re

with open("compiler/semantic/analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

new_builtins = """            ("math_sqrt", 1), ("tensor_matmul", 2), ("ml_kmeans_fit", 3), ("ml_kmeans_predict", 2),"""
content = content.replace('("print", -1),', '("print", -1),\n' + new_builtins)

with open("compiler/semantic/analyzer.py", "w", encoding="utf-8") as f:
    f.write(content)
