
path = "C:/Users/ayush/.gemini/antigravity/brain/3daae0d9-538b-467d-b594-5c2e7b283147/task.md"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("- [ ] Write Test Suite", "- [x] Write Test Suite")
c = c.replace("- [ ] Positive Type Tests", "- [x] Positive Type Tests")
c = c.replace("- [ ] Negative Type Tests", "- [x] Negative Type Tests")
c = c.replace("- [ ] Stitch into `run.py` pipeline", "- [x] Stitch into `run.py` pipeline")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

