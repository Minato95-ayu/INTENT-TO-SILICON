import os
import re

def fix_model_colons(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception:
        return

    # Let's find model Name { ... } and insert colons between field name and type
    # Field definitions look like "    name String" or "    is_active Bool = true"
    lines = text.split('\n')
    new_lines = []
    in_model = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('model ') and stripped.endswith('{'):
            in_model = True
            new_lines.append(line)
        elif in_model and stripped == '}':
            in_model = False
            new_lines.append(line)
        elif in_model and len(stripped) > 0 and not stripped.startswith('#'):
            # It's a field! Let's see if it's "name String"
            # It might already have a colon "name: String"
            if ':' not in stripped:
                # Insert a colon after the first word
                parts = stripped.split(' ', 1)
                if len(parts) == 2:
                    new_line = line.replace(parts[0] + ' ' + parts[1], parts[0] + ': ' + parts[1], 1)
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

for root, dirs, files in os.walk('examples'):
    for file in files:
        if file.endswith('.aayu'):
            fix_model_colons(os.path.join(root, file))

# And test files too
for root, dirs, files in os.walk('tests'):
    for file in files:
        if file.endswith('.aayu'):
            fix_model_colons(os.path.join(root, file))
