def handle_hover(msg, workspace, protocol):
    uri = msg["params"]["textDocument"]["uri"]
    position = msg["params"]["position"]
    
    doc = workspace.get_document(uri)
    if not doc:
        return
        
    line_idx = position["line"]
    char_idx = position["character"]
    
    # Simple word extractor
    lines = doc.text.split("\n")
    if line_idx >= len(lines):
        return
        
    line_text = lines[line_idx]
    
    # Find word boundaries
    start = min(char_idx, len(line_text) - 1) if line_text else 0
    while start > 0 and (line_text[start-1].isalnum() or line_text[start-1] == '_'):
        start -= 1
        
    end = char_idx
    while end < len(line_text) and (line_text[end].isalnum() or line_text[end] == '_'):
        end += 1
        
    word = line_text[start:end]
    
    if not word:
        protocol.write_message({"jsonrpc": "2.0", "id": msg["id"], "result": None})
        return
        
    # Dictionary of standard AAYU types and keywords
    doc_map = {
        "page": "**page**\n\nDefines a top-level route/page in the application.",
        "component": "**component**\n\nDefines a reusable UI block.",
        "state": "**state**\n\nDeclares a reactive state variable.",
        "action": "**action**\n\nDeclares an action block or function.",
        "container": "**container**\n\nA layout block that wraps children.",
        "text": "**text**\n\nA UI component for rendering string content.",
        "button": "**button**\n\nA clickable UI widget.",
        "input": "**input**\n\nA text input field.",
    }
    
    info = doc_map.get(word, f"**{word}**\n\nAAYU Language Construct.")
    
    response = {
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "contents": {
                "kind": "markdown",
                "value": info
            }
        }
    }
    protocol.write_message(response)
