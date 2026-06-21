import os

os.makedirs('apm-test/.aayu/packages/auth', exist_ok=True)

with open('apm-test/.aayu/packages/auth/main.aayu', 'w', encoding='utf-8') as f:
    f.write('task login with req.\n    return "Login Success!".\nend.\n')

with open('apm-test/main.aayu', 'w', encoding='utf-8') as f:
    f.write('use "auth".\nserve on 8081.\nget "/login" to login.\n')
