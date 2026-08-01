import re

with open('scratch/test_http.py', 'r') as f:
    content = f.read()

content = content.replace('{"name": "AAYU", "goal": "Intent-to-Silicon"}', '{name: "AAYU", goal: "Intent-to-Silicon"}')

with open('scratch/test_http.py', 'w') as f:
    f.write(content)
