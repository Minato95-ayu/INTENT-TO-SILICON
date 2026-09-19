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

﻿import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests\test_phase74_package_manager.py'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Stripped BOM")
