import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen("http://localhost:3000/")
    print(response.read().decode('utf-8'))
except urllib.error.URLError as e:
    print(f"Error: {e}")
