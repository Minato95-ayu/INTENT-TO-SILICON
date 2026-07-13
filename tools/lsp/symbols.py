def handle_workspace_symbol(msg, workspace, protocol):
    query = msg["params"].get("query", "")
    # Stub: Return empty list of symbols matching query
    protocol.write_message({
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": []
    })
