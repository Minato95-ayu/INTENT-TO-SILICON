import re

with open('examples/flipkart_clone.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace db::insert with native insert
text = re.sub(r'db::insert\("Product", \{\s*"title":\s*([^,]+),\s*"price":\s*([^,]+),\s*"rating":\s*([^\}]+)\s*\}\)', r'insert Product { title = \1, price = \2, rating = \3 }', text)
text = re.sub(r'db::insert\("CartItem", \{\s*"title":\s*([^,]+),\s*"price":\s*([^\}]+)\s*\}\)', r'insert CartItem { title = \1, price = \2 }', text)

with open('examples/flipkart_clone.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
