import urllib.request
try:
    r = urllib.request.urlopen('http://127.0.0.1:4001/')
    print(r.getcode())
except Exception as e:
    print("Error:", e)