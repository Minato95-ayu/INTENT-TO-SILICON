import re
import os

def convert_md_to_latex(md_filepath, tex_filepath):
    with open(md_filepath, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 1. LaTeX Preamble
    latex_preamble = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{enumitem}

\title{Intent-to-Silicon: Ambiguity Reduction in Natural Language to Software Specification Translation}
\author{Ayush Kumar Mishra (Ayush Kaushik)}
\date{June 2026}

\begin{document}

\maketitle
"""

    # 2. Extract Abstract
    # Assumes Abstract starts with ## Abstract and ends at the first --- or next ##
    abstract_match = re.search(r'## Abstract\n(.*?)(?=\n---|\n##)', md_text, re.DOTALL)
    abstract_content = ""
    if abstract_match:
        abstract_content = abstract_match.group(1).strip()
        md_text = md_text.replace(abstract_match.group(0), "") # Remove abstract from main text

    # Remove the metadata block at the top if present
    md_text = re.sub(r'# Intent-to-Silicon.*?\n\*\*Author:\*\*.*?\n\*\*Date:\*\*.*?\n', '', md_text, flags=re.DOTALL)
    md_text = re.sub(r'---', '', md_text) # Remove horizontal rules

    # 3. Simple regex replacements
    # Headers
    md_text = re.sub(r'^### (.*?)$', r'\\subsection{\1}', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^## (.*?)$', r'\\section{\1}', md_text, flags=re.MULTILINE)
    
    # Bold text
    md_text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', md_text)
    
    # Inline code
    md_text = re.sub(r'`(.*?)`', r'\\texttt{\1}', md_text)
    
    # Escape percentage signs (excluding those already escaped or formatting commands)
    md_text = re.sub(r'(?<!\\)%', r'\\%', md_text)
    
    # Lists (simple bullet points)
    # This is a basic implementation, replacing lines starting with "- " or "* "
    lines = md_text.split('\n')
    in_list = False
    new_lines = []
    
    for line in lines:
        match = re.match(r'^[\-\*] (.*)$', line)
        if match:
            if not in_list:
                new_lines.append(r'\begin{itemize}')
                in_list = True
            new_lines.append(rf'    \item {match.group(1)}')
        else:
            if in_list and line.strip() == "":
                new_lines.append(r'\end{itemize}')
                in_list = False
            new_lines.append(line)
            
    if in_list:
        new_lines.append(r'\end{itemize}')
        
    latex_body = "\n".join(new_lines)
    
    # Clean up empty itemize environments if any
    latex_body = re.sub(r'\\begin\{itemize\}\s*\\end\{itemize\}', '', latex_body)

    # 4. Assemble Final LaTeX
    final_latex = latex_preamble
    
    if abstract_content:
        # Convert any bold/code in abstract
        abstract_content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', abstract_content)
        abstract_content = re.sub(r'`(.*?)`', r'\\texttt{\1}', abstract_content)
        final_latex += "\\begin{abstract}\n" + abstract_content + "\n\\end{abstract}\n\n"
        
    final_latex += latex_body
    final_latex += "\n\\end{document}\n"

    # Save to file
    with open(tex_filepath, 'w', encoding='utf-8') as f:
        f.write(final_latex)
        
    print(f"Successfully converted {md_filepath} to {tex_filepath}")

if __name__ == "__main__":
    md_path = "paper/Intent_to_Silicon_v2.md"
    tex_path = "paper/main.tex"
    if os.path.exists(md_path):
        convert_md_to_latex(md_path, tex_path)
    else:
        print(f"Error: {md_path} not found.")
