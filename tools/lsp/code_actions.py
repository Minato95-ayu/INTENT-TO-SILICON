def handle_code_action(msg, workspace, protocol):
    uri = msg["params"]["textDocument"]["uri"]
    
    # Stub: Return Quick Fixes
    protocol.write_message({
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": []
    })
