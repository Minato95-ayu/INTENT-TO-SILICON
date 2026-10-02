import re

with open('AAYU_LANGUAGE_HANDBOOK_V1.md', 'r', encoding='utf-8') as f:
    text = f.read()

old_sec6 = """# 3. AI / Math (Native)
let data_x = [1, 2, 3]
let data_y = [2, 4, 6]
let prediction = ai::linear_regression(data_x, data_y)"""
new_sec6 = """# 3. AI / Math (Native)
let data_x = [1, 2, 3]
let data_y = [2, 4, 6]
let prediction = ml::linear_regression_fit(data_x, data_y, 100)"""
text = text.replace(old_sec6, new_sec6)

with open('AAYU_LANGUAGE_HANDBOOK_V1.md', 'w', encoding='utf-8') as f:
    f.write(text)
