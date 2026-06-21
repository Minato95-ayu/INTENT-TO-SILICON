import json
data = json.load(open('test_crud.ayc', 'r'))
print("CONSTANTS:", data['constants'])
print("NAMES:", data['names'])
print("INSTRUCTIONS:")
for i in data['instructions']:
    print(i)
