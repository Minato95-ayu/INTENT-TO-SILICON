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
import re

def fix_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('(e: any)', '(e: unknown)')
    content = content.replace(': any', ': unknown')
    
    # Simple fix for unescaped entities outside tags:
    content = content.replace(\"'\", \"&apos;\")
    content = content.replace(\"'\", \"&apos;\")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('website'):
    for f in files:
        if f.endswith('.tsx') or f.endswith('.ts'):
            fix_file(os.path.join(root, f))
