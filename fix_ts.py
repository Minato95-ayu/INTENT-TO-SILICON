import re

with open("website/app/roadmap/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the array definition
content = content.replace("const phases = [", "const phases: Phase[] = [")

with open("website/app/roadmap/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("roadmap/page.tsx fixed TypeScript error")
