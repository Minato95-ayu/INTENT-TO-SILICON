import json

def apply_replace(content, start_line, end_line, target_content, replacement_content):
    lines = content.split('\n')
    # 1-indexed to 0-indexed
    start_idx = start_line - 1
    end_idx = end_line
    
    new_lines = lines[:start_idx] + replacement_content.split('\n') + lines[end_idx:]
    return '\n'.join(new_lines)

content = ""
with open(r'C:\Users\ayush\.gemini\antigravity\brain\f04cdae4-1492-46f5-ad96-0c000ac1eeba\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='replace') as f:
    for line in f:
        if 'interpreter.py' not in line:
            continue
        try:
            step = json.loads(line)
        except:
            continue
            
        if 'tool_calls' in step:
            for tc in step['tool_calls']:
                args = tc.get('args', {})
                target = args.get('TargetFile', '')
                if 'interpreter.py' in target:
                    if tc['name'] == 'write_to_file':
                        content = args.get('CodeContent', '')
                        print(f"Applied write_to_file (len {len(content)})")
                    elif tc['name'] == 'replace_file_content':
                        start = args.get('StartLine')
                        end = args.get('EndLine')
                        replacement = args.get('ReplacementContent', '')
                        target_content = args.get('TargetContent', '')
                        if start is not None and end is not None:
                            content = apply_replace(content, start, end, target_content, replacement)
                            print(f"Applied replace_file_content lines {start}-{end}")
                    elif tc['name'] == 'multi_replace_file_content':
                        chunks = args.get('ReplacementChunks', [])
                        if not chunks:
                            continue
                        if isinstance(chunks, str):
                            try:
                                chunks = json.loads(chunks)
                            except:
                                pass
                        if isinstance(chunks, list):
                            chunks_sorted = sorted(chunks, key=lambda c: c.get('StartLine', 0), reverse=True)
                            for chunk in chunks_sorted:
                                start = chunk.get('StartLine')
                                end = chunk.get('EndLine')
                                replacement = chunk.get('ReplacementContent', '')
                                target_content = chunk.get('TargetContent', '')
                                if start is not None and end is not None:
                                    content = apply_replace(content, start, end, target_content, replacement)
                                    print(f"Applied chunk lines {start}-{end}")

with open('runtime/vm/interpreter_restored.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved to interpreter_restored.py")
