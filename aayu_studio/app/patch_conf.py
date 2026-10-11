import json
with open('../src-tauri/tauri.conf.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
data['productName'] = 'AAYU Studio'
with open('../src-tauri/tauri.conf.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
