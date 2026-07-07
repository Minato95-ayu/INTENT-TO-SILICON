# Web Development

AAYU eliminates the boundary between backend and frontend. The language natively understands web concepts like routing, requests, views, and server states.

## The HTTP Module

By invoking the `use http.` module, AAYU unlocks its internal HTTP server engine. 

```aayu
use http.

task main.
    serve on 8080.
end.
```

The `serve on 8080.` command binds AAYU to the given port and begins accepting requests natively. AAYU's VM spins up isolated, thread-safe Sub-VM instances for every incoming request, ensuring zero variable leaking between web sessions.

## Custom Routing

You can declare specific REST routes natively without any framework boilerplate. 

```aayu
use http.

get "/hello".
    print "Handling GET request".
    render "home".
end.

post "/submit".
    text name.
    get_form "name" into name.
    print name.
end.

task main.
    serve on 8080.
end.
```

## Auto-CRUD Generation

Writing repetitive Create, Read, Update, Delete routes is a thing of the past. If you declare an Entity, AAYU can auto-generate the complete backend routes and frontend UI screens for it using a single line of code.

```aayu
use http.
use db.

entity Student.
    text name.
    number age.
end.

# This single line generates the REST APIs and UI Admin panel!
crud Student.

task main.
    serve on 8080.
end.
```

Navigate to `/student` on your browser, and you will see a fully functioning, styled dashboard to manage `Student` records!
