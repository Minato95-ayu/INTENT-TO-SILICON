with open('tools/builder/targets/windows.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_build = '''        try:
            subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--console", "--distpath", out_dir, "--name", "app", boot_path], check=True, capture_output=True)
        except Exception as e:
            raise e'''

new_build = '''        try:
            res = subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--console", "--distpath", out_dir, "--name", "app", boot_path], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print("PyInstaller STDOUT:", e.stdout)
            print("PyInstaller STDERR:", e.stderr)
            raise e'''

content = content.replace(old_build, new_build)

with open('tools/builder/targets/windows.py', 'w', encoding='utf-8') as f:
    f.write(content)
