import json
import os

def apply_replace(content, start_line, end_line, target_content, replacement_content):
    lines = content.split('\n')
    # 1-indexed to 0-indexed
    start_idx = start_line - 1
    end_idx = end_line
    
    new_lines = lines[:start_idx] + replacement_content.split('\n') + lines[end_idx:]
    return '\n'.join(new_lines)

# Start with a blank string since the very first tool call in Sprints was likely write_to_file,
# OR we can just extract the largest write_to_file which should be the base.
content = ""

# Actually, the file might have been built iteratively.
# But there was a `write_to_file` of length 26066? Let's find out!
with open(r'C:\Users\ayush\.gemini\antigravity\brain\f04cdae4-1492-46f5-ad96-0c000ac1eeba\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='replace') as f:
    for line in f:
        # Ignore tool calls made by my own restore scripts in scratch/
        if 'restore_interpreter' in line or 'patch_interpreter' in line:
            continue
            
        try:
            step = json.loads(line)
        except:
            continue
            
        if 'tool_calls' in step:
            for tc in step['tool_calls']:
                args = tc.get('args', {})
                target = args.get('TargetFile', '')
                # MUST exactly match the interpreter file
                if 'runtime\\vm\\interpreter.py' in target or 'runtime/vm/interpreter.py' in target:
                    if tc['name'] == 'write_to_file':
                        content = args.get('CodeContent', '')
                        print(f"Applied write_to_file (len {len(content)}) at step {step['step_index']}")
                    elif tc['name'] == 'replace_file_content':
                        start = args.get('StartLine')
                        end = args.get('EndLine')
                        replacement = args.get('ReplacementContent', '')
                        target_content = args.get('TargetContent', '')
                        if start is not None and end is not None:
                            content = apply_replace(content, start, end, target_content, replacement)
                            print(f"Applied replace_file_content lines {start}-{end} at step {step['step_index']}")
                    elif tc['name'] == 'multi_replace_file_content':
                        # Stop at step 4199 which corrupted the file!
                        if step['step_index'] >= 4199:
                            print(f"SKIPPING corrupting step {step['step_index']}")
                            continue
                            
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
                                    print(f"Applied chunk lines {start}-{end} at step {step['step_index']}")

with open('runtime/vm/interpreter_restored.py', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Saved to interpreter_restored.py, final length {len(content)}")
