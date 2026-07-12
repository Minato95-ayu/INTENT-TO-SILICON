import os

cli_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tools\cli.py'
with open(cli_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('✅', '[OK]')
content = content.replace('✨', '[DONE]')

with open(cli_path, 'w', encoding='utf-8') as f:
    f.write(content)

fmt_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tools\formatter.py'
with open(fmt_path, 'r', encoding='utf-8') as f:
    fmt_content = f.read()

fmt_content = fmt_content.replace('if stripped == "end.":', 'if stripped in ["end", "end."]:')

with open(fmt_path, 'w', encoding='utf-8') as f:
    f.write(fmt_content)

print("Fixed emojis and formatter dedent rule.")
