import urllib.request
import urllib.parse
import http.cookiejar
from urllib.error import HTTPError

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

print("1. Registering...")
req1 = urllib.request.Request('http://localhost:8081/register', data=urllib.parse.urlencode({'email':'test@test.com','password':'pw'}).encode())
try:
    print('Register:', opener.open(req1).read().decode())
except HTTPError as e:
    print('Register Error:', e.read().decode())

print("2. Trying Dashboard without login (should fail)")
try:
    req_dash1 = urllib.request.Request('http://localhost:8081/dashboard')
    print('Dashboard:', opener.open(req_dash1).read().decode())
except HTTPError as e:
    print('Dashboard Error:', e.code)

print("3. Logging in...")
req2 = urllib.request.Request('http://localhost:8081/login', data=urllib.parse.urlencode({'email':'test@test.com','password':'pw'}).encode())
try:
    print('Login:', opener.open(req2).read().decode())
except HTTPError as e:
    print('Login Error:', e.read().decode())

print('Cookies:', [c.name for c in cj])

print("4. Dashboard after login")
try:
    req3 = urllib.request.Request('http://localhost:8081/dashboard')
    print('Dashboard:', opener.open(req3).read().decode())
except HTTPError as e:
    print('Dashboard Error:', e.read().decode())

print("5. Logout")
req4 = urllib.request.Request('http://localhost:8081/logout', data=b'')
try:
    print('Logout:', opener.open(req4).read().decode())
except HTTPError as e:
    print('Logout Error:', e.read().decode())

print("6. Dashboard after logout")
try:
    opener.open(urllib.request.Request('http://localhost:8081/dashboard'))
except HTTPError as e:
    print('Dashboard after logout Error:', e.code)
