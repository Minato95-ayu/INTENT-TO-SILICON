
with open("compiler/semantic/analyzer.py", "r", encoding="utf-8") as f:
    code = f.read()
code = code.replace("(\"math::ceil\", 1)", "(\"math::ceil\", 1), (\"ai::train\", 1), (\"ai::predict\", 1), (\"ml::kmeans\", 2)")
with open("compiler/semantic/analyzer.py", "w", encoding="utf-8") as f:
    f.write(code)

