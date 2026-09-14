import re

with open("runtime/stdlib/stdlib.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add registration in __init__
register_str = """
        register_math_lib(self.registry)
        register_ai_lib(self.registry)
"""

new_register_str = register_str + """
        # Register ML explicitly
        self.registry.register("ml_kmeans_fit", self.ml_kmeans_fit)
        self.registry.register("ml_kmeans_predict", self.ml_kmeans_predict)
        self.registry.register("ml_linear_regression_fit", self.ml_linear_regression_fit)
        self.registry.register("ml_linear_regression_predict", self.ml_linear_regression_predict)
"""

content = content.replace(register_str, new_register_str)

with open("runtime/stdlib/stdlib.py", "w", encoding="utf-8") as f:
    f.write(content)
print("stdlib.py updated with ML registration")
