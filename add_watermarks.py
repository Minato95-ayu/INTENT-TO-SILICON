import os

HEADER = '''# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================
'''

def watermark_files(directory):
    count = 0
    for root, _, files in os.walk(directory):
        if '.venv' in root or '__pycache__' in root or '.git' in root or 'build' in root or 'dist' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(filepath, 'r', encoding='latin1') as f:
                            content = f.read()
                    except:
                        continue
                
                if "COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK" not in content:
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(HEADER + "\n" + content)
                        count += 1
                    except:
                        pass
    return count

if __name__ == '__main__':
    c = watermark_files('.')
    print(f"Added watermark to {c} Python files.")
