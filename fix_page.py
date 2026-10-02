import re
with open("website/app/page.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(
    r"\{line\.replace\([^\)]+\)\}",
    "{line}",
    text
)

with open("website/app/page.tsx", "w", encoding="utf-8") as f:
    f.write(text)
