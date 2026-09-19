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

with open('examples/mit_nexus_ai.aayu', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('ai_generate(', 'ai::generate(')
with open('examples/mit_nexus_ai.aayu', 'w', encoding='utf-8') as f:
    f.write(code)

with open('runtime/stdlib/modules/ai_lib.py', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('"ai_generate"', '"ai::generate"')
with open('runtime/stdlib/modules/ai_lib.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('compiler/semantic/analyzer.py', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('"ai_generate"', '"ai::generate"')
with open('compiler/semantic/analyzer.py', 'w', encoding='utf-8') as f:
    f.write(code)
