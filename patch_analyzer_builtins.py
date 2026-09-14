import re

with open("compiler/semantic/analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

old_builtins = '''        builtins = [
            ("print", -1),
            ("math_sqrt", 1), ("tensor_matmul", 2), ("ml_kmeans_fit", 3), ("ml_kmeans_predict", 2),
            ("HTTP.get", 1), ("HTTP.post", 2),
            ("file::read", 1), ("file::write", 2),
            ("Regex.match", 2),
            ("json::parse", 1), ("json::stringify", 1),
            ("Storage.insert", 2), ("Storage.find", 2),
            ("len", 1), ("append", 2), ("push", 2), ("remove", 2), ("has", 2), ("keys", 1), ("values", 1), ("typeof", 1), ("db::query", 1), ("auth::login", 2),
            ("math::sin", 1), ("math::cos", 1), ("math::tan", 1), ("math::sqrt", 1), ("math::pow", 2),
            ("math::abs", 1), ("math::round", 1), ("math::min", 2), ("math::max", 2),
            ("math::floor", 1), ("math::ceil", 1), ("ai::train", 1), ("ai::predict", 1), ("ml::kmeans", 2)
        ]'''

new_builtins = '''        builtins = [
            ("print", -1),
            ("len", 1), ("append", 2), ("push", 2), ("remove", 2), ("has", 2), ("keys", 1), ("values", 1), ("typeof", 1),
            ("db::connect", 1), ("db::query", 2), ("db::execute", 2),
            ("http::get", 1), ("http::post", 2),
            ("ml::kmeans_fit", 3), ("ml::kmeans_predict", 2),
            ("ml::linear_regression_fit", 3), ("ml::linear_regression_predict", 2),
            ("file::read", 1), ("file::write", 2),
            ("json::parse", 1), ("json::stringify", 1),
            ("math::sin", 1), ("math::cos", 1), ("math::tan", 1), ("math::sqrt", 1), ("math::pow", 2),
            ("math::abs", 1), ("math::round", 1), ("math::min", 2), ("math::max", 2),
            ("math::floor", 1), ("math::ceil", 1)
        ]'''

content = content.replace(old_builtins, new_builtins)

with open("compiler/semantic/analyzer.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated semantic analyzer builtins.")
