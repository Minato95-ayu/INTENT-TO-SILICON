import re

with open("website/app/roadmap/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the type definition that was accidentally overwritten
content = content.replace('status: "in-progress" | "in-progress" | "planned";', 'status: "completed" | "in-progress" | "planned";')

with open("website/app/roadmap/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("roadmap/page.tsx type fixed")
