import sys
with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace(
    "[[b'content-type', b'text/event-stream'],",
    "[(b'content-type', b'text/event-stream'),"
)
code = code.replace(
    "[b'cache-control', b'no-cache'],",
    "(b'cache-control', b'no-cache'),"
)
code = code.replace(
    "[b'connection', b'keep-alive'],\n                ] + ([[b'set-cookie', f'session_id={session.session_id}; Path=/'.encode()]] if session_id != session.session_id else [])",
    "(b'connection', b'keep-alive'),\n                ] + ([(b'set-cookie', f'session_id={session.session_id}; Path=/'.encode())] if session_id != session.session_id else [])"
)
code = code.replace(
    "[[b'content-type', b'application/json']]",
    "[(b'content-type', b'application/json')]"
)
code = code.replace(
    "[[b'content-type', (mime_type or 'application/octet-stream').encode()]]",
    "[(b'content-type', (mime_type or 'application/octet-stream').encode())]"
)
with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.write(code)