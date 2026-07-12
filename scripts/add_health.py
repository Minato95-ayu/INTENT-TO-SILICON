import os

api_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\api\main.py'
with open(api_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "@app.get('/health')" not in content:
    content = content.replace('class CompileRequest', '''
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

class CompileRequest''')
    with open(api_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Added health route")
