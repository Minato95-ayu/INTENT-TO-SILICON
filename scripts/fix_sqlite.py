import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests\test_phase76_stdlib_database.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('def test_sqlite(self):', 'def test_sqlite(self):\n        import os\n        if os.path.exists("test.db"): os.remove("test.db")')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed sqlite test")
