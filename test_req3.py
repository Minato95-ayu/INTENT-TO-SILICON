import urllib.request
try:
    r = urllib.request.urlopen('http://127.0.0.1:4003/')
    print(r.read())
except Exception as e:
    print("Error:", e)