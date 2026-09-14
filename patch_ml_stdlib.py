import re

with open("runtime/stdlib/stdlib.py", "r", encoding="utf-8") as f:
    content = f.read()

import_str = "import json\nimport uuid\nimport urllib.request\nimport urllib.parse\nimport csv\nfrom http.server import HTTPServer, BaseHTTPRequestHandler"
new_import_str = import_str + "\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom modules.ml import ml_kmeans_fit, ml_kmeans_predict, ml_linear_regression_fit, ml_linear_regression_predict"
content = content.replace(import_str, new_import_str)

class_methods_insert = """
    def ml_kmeans_fit(self, data: list, k: int = 3, max_iters: int = 100) -> int:
        return ml_kmeans_fit(data, k, max_iters)

    def ml_kmeans_predict(self, model_id: int, data: list) -> list:
        return ml_kmeans_predict(model_id, data)

    def ml_linear_regression_fit(self, X: list, y: list, lr: float = 0.01, epochs: int = 1000) -> int:
        return ml_linear_regression_fit(X, y, lr, epochs)

    def ml_linear_regression_predict(self, model_id: int, X: list) -> list:
        return ml_linear_regression_predict(model_id, X)
"""

# Let's insert the methods before def json_serialize
content = content.replace("    def json_serialize(self,", class_methods_insert + "\n    def json_serialize(self,")

with open("runtime/stdlib/stdlib.py", "w", encoding="utf-8") as f:
    f.write(content)
print("stdlib.py updated with ML methods")
