
path = "C:/Users/ayush/.gemini/antigravity/brain/3daae0d9-538b-467d-b594-5c2e7b283147/task.md"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("- [ ] Upgrade Symbol Table", "- [x] Upgrade Symbol Table")
c = c.replace("- [ ] Upgrade TypeError", "- [x] Upgrade TypeError")
c = c.replace("- [ ] Implement Type Inference pass", "- [x] Implement Type Inference pass")
c = c.replace("- [ ] State variable inference", "- [x] State variable inference")
c = c.replace("- [ ] Literal/Expression inference", "- [x] Literal/Expression inference")
c = c.replace("- [ ] Implement Type Checker pass", "- [x] Implement Type Checker pass")
c = c.replace("- [ ] Validations for State Assignment", "- [x] Validations for State Assignment")
c = c.replace("- [ ] Validations for Binary/Unary Ops", "- [x] Validations for Binary/Unary Ops")
c = c.replace("- [ ] Validations for Widget Props", "- [x] Validations for Widget Props")
c = c.replace("- [ ] Validations for Function/Route Returns", "- [x] Validations for Function/Route Returns")
c = c.replace("- [ ] Validations for Model Field access", "- [x] Validations for Model Field access")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

