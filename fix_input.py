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

code = code.replace('Input placeholder="Type your message here..." bind=user_input', 
'''Input placeholder="Type your message here..."
                bind user_input
            end''')

with open('examples/mit_nexus_ai.aayu', 'w', encoding='utf-8') as f:
    f.write(code)
