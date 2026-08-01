
import os
for file in ["stthomas_app/pages/home.aayu", "stthomas_app/pages/notices.aayu"]:
    p = os.path.join("D:/intent-to-silicon-research/INTENT-TO-SILICON", file)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
        if "page Home" in c:
            c = c.replace("page Home", "component Home")
        if "page NoticesList" in c:
            c = c.replace("page NoticesList", "component NoticesList")
        with open(p, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Patched {file}")

