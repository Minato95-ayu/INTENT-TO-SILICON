import urllib.request
import urllib.parse
import http.cookiejar
from urllib.error import HTTPError
import json

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
base = 'http://localhost:8082'

def test(name, req, expected_status=200):
    print(f"[{name}]", end=" ")
    try:
        resp = opener.open(req)
        body = resp.read().decode()
        print(f"OK (Status {resp.code})")
        return body
    except HTTPError as e:
        print(f"FAILED (Status {e.code})")
        return None

# 1. Dashboard without login -> 401
test("Dashboard No Login", urllib.request.Request(f"{base}/dashboard"), 401)

# 2. Setup Admin
test("Setup Admin", urllib.request.Request(f"{base}/setup"))

# 3. Login
login_data = urllib.parse.urlencode({'email':'admin@library.com','password':'admin'}).encode()
test("Login", urllib.request.Request(f"{base}/login_process", data=login_data))

# 3. Create Book
book_data = urllib.parse.urlencode({'title':'The Pragmatic Programmer','author':'Andy Hunt','isbn':'978-0201616224'}).encode()
test("Add Book", urllib.request.Request(f"{base}/books/add", data=book_data))

# 4. Create Student
student_data = urllib.parse.urlencode({'name':'John Doe','email':'john@doe.com','student_id':'S12345'}).encode()
test("Add Student", urllib.request.Request(f"{base}/students/add", data=student_data))

# 5. Check APIs
books_json = test("API Books", urllib.request.Request(f"{base}/api/books"))
students_json = test("API Students", urllib.request.Request(f"{base}/api/students"))

try:
    books = json.loads(books_json)
    students = json.loads(students_json)
    print("Books JSON:", json.dumps(books, indent=2))
    print("Students JSON:", json.dumps(students, indent=2))
    
    if len(books) > 0 and len(students) > 0:
        book_id = books[0]['id']
        student_id = students[0]['id']
        
        # 6. Issue Book
        issue_data = urllib.parse.urlencode({'book_id': book_id, 'student_id': student_id}).encode()
        test("Issue Book", urllib.request.Request(f"{base}/issue_process", data=issue_data))
        
        # 7. Check if book status is Issued
        books_after = json.loads(test("API Books After Issue", urllib.request.Request(f"{base}/api/books")))
        print("Book Status:", books_after[0]['status'])
        
        # We don't have an API for issues yet, but we can verify it's working by checking dashboard
        dashboard_html = test("Dashboard", urllib.request.Request(f"{base}/dashboard"))
        if "Books Issued</h3>" in dashboard_html:
            print("Dashboard loads successfully.")
            
except Exception as e:
    print("Error parsing/testing:", e)

# 8. Logout
test("Logout", urllib.request.Request(f"{base}/logout"))

