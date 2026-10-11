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

﻿import os, re

def fix_quotes(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue with brainos/page.tsx line 11:
    content = content.replace('{{/* Internal State Simulation */}}', '{/* Internal State Simulation */}')
    content = content.replace('{{/* AAYU Compiler passes */}}', '{/* AAYU Compiler passes */}')
    content = content.replace('{{/* Execution output will appear here */}}', '{/* Execution output will appear here */}')

    # And if I replaced without curly braces but it was already in {}:
    content = content.replace('{/* {/*', '{/*')
    content = content.replace('*/} */}', '*/}')

    # Missing braces around comments:
    content = re.sub(r'(?<!\{)// AAYU', '{/* AAYU', content)
    
    # Let's just fix the rest using generic replace for common quotes
    content = content.replace('"', '&quot;')
    # BUT wait, this breaks JSX attributes like className="text-xl"
