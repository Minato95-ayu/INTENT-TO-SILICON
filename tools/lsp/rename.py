def handle_rename(msg, workspace, protocol):
    uri = msg["params"]["textDocument"]["uri"]
    position = msg["params"]["position"]
    new_name = msg["params"]["newName"]
    
    doc = workspace.get_document(uri)
    if not doc:
        protocol.write_message({"jsonrpc": "2.0", "id": msg["id"], "result": None})
        return
        
    line_idx = position["line"]
    char_idx = position["character"]
    
    lines = doc.text.split("\n")
    if line_idx >= len(lines):
        protocol.write_message({"jsonrpc": "2.0", "id": msg["id"], "result": None})
        return
        
    line_text = lines[line_idx]
    
    start = char_idx
    while start > 0 and (line_text[start-1].isalnum() or line_text[start-1] == '_'):
        start -= 1
        
    end = char_idx
    while end < len(line_text) and (line_text[end].isalnum() or line_text[end] == '_'):
        end += 1
        
    old_word = line_text[start:end]
    if not old_word:
        protocol.write_message({"jsonrpc": "2.0", "id": msg["id"], "result": None})
        return
        
    # Find all occurrences of old_word in the document (Simplistic token replace for RC0)
    edits = []
    for i, line in enumerate(lines):
        idx = 0
        while True:
            idx = line.find(old_word, idx)
            if idx == -1:
                break
            
            # Check boundaries
            is_start_bound = idx == 0 or not (line[idx-1].isalnum() or line[idx-1] == '_')
            is_end_bound = idx + len(old_word) == len(line) or not (line[idx + len(old_word)].isalnum() or line[idx + len(old_word)] == '_')
            
            if is_start_bound and is_end_bound:
                edits.append({
                    "range": {
                        "start": {"line": i, "character": idx},
                        "end": {"line": i, "character": idx + len(old_word)}
                    },
                    "newText": new_name
                })
            idx += len(old_word)
            
    protocol.write_message({
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "changes": {
                uri: edits
            }
        }
    })
