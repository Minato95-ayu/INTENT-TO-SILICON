import re

with open('tests/test_smoke.py', 'r', encoding='utf-8') as f:
    text = f.read()

get_button_func = """
        def get_button_id(node):
            if node.get("type") == "button":
                return node.get("id")
            for child in node.get("children", []):
                val = get_button_id(child)
                if val is not None:
                    return val
            return None
"""

text = text.replace('self.assertEqual(str(get_text_value(tree)), "Count is: ")', get_button_func + '\n        self.assertEqual(str(get_text_value(tree)), "Count is: ")')

with open('tests/test_smoke.py', 'w', encoding='utf-8') as f:
    f.write(text)
