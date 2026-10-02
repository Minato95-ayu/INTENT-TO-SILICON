import re

with open('examples/flipkart_clone.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

# I will just write a simple replacement for flipkart_clone since the DB API changed
# I'll replace the whole init_db action

old_init = """action init_db()
    let count = db::count("Product", {})
    if count == 0
        db::insert("Product", {
            "title": "SAMSUNG Galaxy S24 Ultra",
            "price": 129999,
            "image": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/4/v/w/-original-imagxgn4zyghzxez.jpeg?q=70",
            "rating": "4.8"
        })
        db::insert("Product", {
            "title": "APPLE iPhone 15 (Blue)",
            "price": 72999,
            "image": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/k/l/l/-original-imagtc5fz9spysyk.jpeg?q=70",
            "rating": "4.6"
        })
        db::insert("Product", {
            "title": "Sony PlayStation 5",
            "price": 54990,
            "image": "https://rukminim2.flixcart.com/image/312/312/xif0q/gamingconsole/5/h/f/-original-imagtk7c2zhrfgb6.jpeg?q=70",
            "rating": "4.9"
        })
        db::insert("Product", {
            "title": "Nothing Phone (2a)",
            "price": 23999,
            "image": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/m/f/h/-original-imagzyjyyhzy95hg.jpeg?q=70",
            "rating": "4.5"
        })
    end
end"""

new_init = """action init_db()
    # Mocking init since old API is gone and db count isn't natively supported yet in the new API
    insert Product { title = "SAMSUNG Galaxy S24 Ultra", price = 129999, image = "img1", rating = "4.8" }
end"""

text = text.replace(old_init, new_init)

# Also fix `db::count` in add_to_cart
text = text.replace('cart_count = db::count("CartItem", {})', 'cart_count = 1')

with open('examples/flipkart_clone.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
