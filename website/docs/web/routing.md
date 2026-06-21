# Routing and Views

AAYU has a built-in web server. You don't need any complex frameworks to start a web application.

```aayu
use http.

task handle_home with req.
    return render "home.html".
end.

route "/" to handle_home.

serve on 8080.
```
