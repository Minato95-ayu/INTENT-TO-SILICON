import re

with open('AAYU_LANGUAGE_HANDBOOK_V1.md', 'r', encoding='utf-8') as f:
    text = f.read()

old_section = """model User
    id Int
    name String
    is_active Bool = true
end

# Usage (Memory + Database instantly synced)
let u = User.new(name: "Ayush")
u.save() # Instantly writes to built-in SQLite

let all_users = User.all() # Fetch from DB"""

new_section = """model User {
    id: Int
    name: String
    is_active: Bool
}

# Usage (Memory + Database instantly synced using native keywords)
insert User { id = 1, name = "Ayush", is_active = true }

# Fetch from DB natively
let all_users = find User"""

if old_section in text:
    text = text.replace(old_section, new_section)
else:
    print("WARNING: Old section not found in handbook")

# Let's also fix list::len if it is there, though I didn't see it.
text = text.replace('list::len', 'list::length')

with open('AAYU_LANGUAGE_HANDBOOK_V1.md', 'w', encoding='utf-8') as f:
    f.write(text)
