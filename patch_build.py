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

with open("tools/builder/targets/windows.py", "r") as f:
    c = f.read()
c = c.replace(b"MOCK_WINDOWS_EXE_CONTENT".decode('utf-8'), "MZ_MOCK_WINDOWS_EXE_CONTENT")
with open("tools/builder/targets/windows.py", "w") as f:
    f.write(c)
