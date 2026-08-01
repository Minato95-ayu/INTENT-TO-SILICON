import sqlite3
try:
    conn = sqlite3.connect("benchmarks/framework_showdown/django_app/db.sqlite3")
    conn.execute("INSERT INTO api_user (email, password, role) VALUES ('admin@shop.com', 'secret', 'admin')")
    conn.commit()
    print("Seeded")
except Exception as e:
    print(e)
