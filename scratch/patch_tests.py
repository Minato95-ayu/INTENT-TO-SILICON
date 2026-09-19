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

with open('tests/regression/run_all_tests.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'subprocess.run(cmd, shell=True, check=True, cwd=cwd)',
    '''
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.abspath(os.getcwd())
        subprocess.run(cmd, shell=True, check=True, cwd=cwd, env=env)
    '''
)

with open('tests/regression/run_all_tests.py', 'w', encoding='utf-8') as f:
    f.write(content)
