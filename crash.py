import urllib.request
import time
import http.cookiejar
import traceback

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

try:
    print('Connect to stream 1')
    resp1 = urllib.request.urlopen('http://localhost:3000/api/stream')
    print('Stream 1 response:', resp1.readline().decode())
    resp1.close()
    
    print('Connect to stream 2')
    resp2 = urllib.request.urlopen('http://localhost:3000/api/stream')
    print('Stream 2 response:', resp2.readline().decode())
    resp2.close()
    
except Exception as e:
    traceback.print_exc()
