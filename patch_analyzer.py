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

import re

with open("compiler/semantic/analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

new_builtins = """            ("math_sqrt", 1), ("tensor_matmul", 2), ("ml_kmeans_fit", 3), ("ml_kmeans_predict", 2),"""
content = content.replace('("print", -1),', '("print", -1),\n' + new_builtins)

with open("compiler/semantic/analyzer.py", "w", encoding="utf-8") as f:
    f.write(content)
