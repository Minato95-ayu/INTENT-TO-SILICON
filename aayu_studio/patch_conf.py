import json
with open('D:/Topptic/package.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
data['name'] = 'aayu-studio'
data['version'] = '1.1.0'
with open('D:/Topptic/package.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

with open('D:/Topptic/src-tauri/tauri.conf.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
data['productName'] = 'AAYU Studio'
with open('D:/Topptic/src-tauri/tauri.conf.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
