import os
import re

def fix_jsx_mangles(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    
    # Fix className={ ... \} mangles
    # This matches className={ followed by anything then \}
    # Be careful not to match too aggressively
    content = re.sub(r'className=\{([^\}]*?)\\\}', r'className={\1}', content)
    
    # Fix }\n at end of files
    content = content.replace('}\\n', '}')
    
    # Specific fixes
    if 'language-content.tsx' in filepath:
        content = content.replace('{enum Result<T, E>', 'enum Result<T, E>')
        
    if 'docs.ts' in filepath:
        content = content.replace('items: DocItem[,', 'items: DocItem[];')
        
    if 'mdx.ts' in filepath:
        content = content.replace('\\.mdx', 'f"{slug}.mdx"')
        content = content.replace('path.join(DOCS_DIR, category, f"{slug}.mdx")', 'path.join(DOCS_DIR, category, f"{slug}.mdx")')
        # Wait, Nextjs is ts not python... backticks!
        content = content.replace('f"{slug}.mdx"', '${slug}.mdx')
        
    if 'download/page.tsx' in filepath:
        content = content.replace('Github', 'GithubIcon')
        content = content.replace('<Github', '<GithubIcon')

    if original != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")

def scan_dir(d):
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.tsx') or file.endswith('.ts'):
                fix_jsx_mangles(os.path.join(root, file))

scan_dir(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website')
