# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

def handle_completion(msg, workspace, protocol):
    uri = msg["params"]["textDocument"]["uri"]
    position = msg["params"]["position"]
    
    # Simple static completion
    completions = [
        {"label": "page", "kind": 14, "detail": "Keyword"},
        {"label": "state", "kind": 14, "detail": "Keyword"},
        {"label": "action", "kind": 14, "detail": "Keyword"},
        {"label": "component", "kind": 14, "detail": "Keyword"},
        {"label": "container", "kind": 7, "detail": "Widget"},
        {"label": "text", "kind": 7, "detail": "Widget"},
        {"label": "button", "kind": 7, "detail": "Widget"},
        {"label": "input", "kind": 7, "detail": "Widget"},
    ]
    
    protocol.write_message({
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": completions
    })
