import os
import shutil

# Copy aayu-http
shutil.copytree('official_packages/aayu-http', 'apm-test/.aayu/packages/http', dirs_exist_ok=True)
# Copy aayu-gemini
shutil.copytree('official_packages/aayu-gemini', 'apm-test/.aayu/packages/gemini', dirs_exist_ok=True)

with open('apm-test/main.aayu', 'w', encoding='utf-8') as f:
    f.write('''use http.

task main.
    res is get_request("https://jsonplaceholder.typicode.com/todos/1").
    body is get "body" from res.
    title is get "title" from body.
    return title.
end.
''')
