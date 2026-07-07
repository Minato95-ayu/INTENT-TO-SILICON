# Building a Todo App

AAYU makes building a web application incredibly simple by combining natural language routing and a built-in web server.

## 1. Intent-to-Silicon (Automatic)

You can build the entire application instantly using the AAYU Intent Engine. Simply run:

```bash
aayu build "Build a Todo App"
```

AAYU will detect your domain, ask any clarifying questions, and generate the full architecture, code, and frontend UI templates for you!

## 2. Manual Construction

If you prefer to write it by hand, create a `main.aayu` file:

```aayu
# Import HTTP and DB packages
use http.
use db.

# Define the Schema
entity Task.
    text title.
    text status.
    text created_at.
end.

# Define the Web Route
task handle_index with req.
    # Get tasks from database
    set "tasks" to db_find("Task", {}).
    
    # Return HTML view
    return render "index.html" with tasks.
end.

route "/" to handle_index.

# Start the Web Server
serve on 8080.
```

Create a `views/index.html` file in the same directory:
```html
<!DOCTYPE html>
<html>
<body>
    <h1>My Todo App</h1>
    <ul>
        {% for task in tasks %}
            <li>{{ task.title }} - {{ task.status }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

Run your app:
```bash
aayu run main.aayu
```
Navigate to `http://localhost:8080`!
