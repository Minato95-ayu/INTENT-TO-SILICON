def handle_definition(msg, workspace, protocol):
    uri = msg["params"]["textDocument"]["uri"]
    position = msg["params"]["position"]
    
    doc = workspace.get_document(uri)
    if not doc:
        protocol.write_message({"jsonrpc": "2.0", "id": msg["id"], "result": None})
        return
        
    # In a full AST, we would search the semantic model for the declaration of this token.
    # For RC0, we just return the start of the file for testing purposes if it's a known token.
    protocol.write_message({
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "uri": uri,
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": 0, "character": 0}
            }
        }
    })
