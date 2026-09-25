import sys
with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace(
    "await send({'type': 'http.response.body', 'body': f.read()})",
    "print('Sending body!')\n                await send({'type': 'http.response.body', 'body': f.read()})\n                print('Body sent!')"
)
code = code.replace(
    "await send({\n                'type': 'http.response.start',",
    "print('Sending start!')\n            await send({\n                'type': 'http.response.start',"
)
with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.write(code)