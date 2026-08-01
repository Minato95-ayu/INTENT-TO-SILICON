import json

with open(r'C:\Users\ayush\.gemini\antigravity\brain\f04cdae4-1492-46f5-ad96-0c000ac1eeba\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='replace') as f:
    for line in f:
        try:
            step = json.loads(line)
        except Exception:
            continue
        
        if step.get('step_index') == 4203:
            content = step.get('content', '')
            with open('scratch/step4203.txt', 'w', encoding='utf-8') as out_f:
                out_f.write(content)
            print("Wrote step4203.txt")
            break
