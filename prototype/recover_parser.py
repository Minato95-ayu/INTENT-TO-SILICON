import json
import re

log_path = r"C:\Users\ayush\.gemini\antigravity\brain\6964e7af-6ba3-4c85-a841-95a37dfd3e94\.system_generated\logs\transcript_full.jsonl"

found_contents = []

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            entry = json.loads(line)
            # check tool responses for view_file of parser.py
            if entry.get("type") == "TOOL_RESPONSE":
                # we don't have tool name directly in some formats, but let's check content
                content = entry.get("content", "")
                if "File Path: `file:///D:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/aayu_language/parser.py`" in content:
                    print(f"Found view_file at step {entry.get('step_index')}")
                    # extracting lines
                    lines = content.splitlines()
                    for l in lines:
                        if l.startswith("The following code has been modified"):
                            continue
            
            # check model tool calls for write_to_file
            if entry.get("type") == "PLANNER_RESPONSE":
                tool_calls = entry.get("tool_calls", [])
                for tc in tool_calls:
                    if tc.get("tool_name") == "default_api:write_to_file":
                        args = tc.get("args", {})
                        if "parser.py" in args.get("TargetFile", ""):
                            print(f"Found write_to_file at step {entry.get('step_index')}")
                            found_contents.append(args.get("CodeContent"))
        except:
            pass

if found_contents:
    print(f"Recovered {len(found_contents)} write_to_file calls.")
    with open("recovered_parser.py", "w", encoding="utf-8") as f:
        f.write(found_contents[-1])
    print("Saved to recovered_parser.py")
else:
    print("No write_to_file found.")
