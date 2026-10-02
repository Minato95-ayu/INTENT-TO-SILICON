import re

with open('AAYU_LANGUAGE_HANDBOOK_V1.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Section 7
old_sec7 = """Page Home
    Column
        Text("My Notes")
        Button("Fetch", onClick: fetchNotes)
    end
end"""

new_sec7 = """Page Home
    Column
        Text "My Notes"
        Button "Fetch" onClick="fetchNotes"
    end
end"""
text = text.replace(old_sec7, new_sec7)

text = text.replace("respond(notes)", "respond notes")

# Fix Section 2 (If/Else needs cores defined)
old_sec2 = """# If / Else
if cores > 4
    print("Fast PC")
elif cores == 4
    print("Normal PC")
else
    print("Slow PC")
end"""
new_sec2 = """# If / Else
let cores = 8
if cores > 4
    print("Fast PC")
elif cores == 4
    print("Normal PC")
else
    print("Slow PC")
end"""
text = text.replace(old_sec2, new_sec2)

# Fix Section 6 (File I/O needs data_x, data_y)
old_sec6 = """# 3. AI / Math (Native)
let prediction = ai::linear_regression(data_x, data_y)"""
new_sec6 = """# 3. AI / Math (Native)
let data_x = [1, 2, 3]
let data_y = [2, 4, 6]
let prediction = ai::linear_regression(data_x, data_y)"""
text = text.replace(old_sec6, new_sec6)

with open('AAYU_LANGUAGE_HANDBOOK_V1.md', 'w', encoding='utf-8') as f:
    f.write(text)
