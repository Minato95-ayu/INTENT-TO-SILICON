import json
with open('package.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
data['name'] = 'aayu-studio'
data['version'] = '1.1.0'
with open('package.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
