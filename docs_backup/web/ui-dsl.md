# UI DSL

AAYU is not just a backend architecture language. It possesses a full **UI Domain Specific Language (DSL)** capable of rendering visual frontends directly from the `.aayu` syntax.

## Pages and Components

You can define standard UI screens using the `page` keyword. Inside a page, you can nest layout components seamlessly.

```aayu
page Dashboard.
    
    card.
        heading "Welcome to Hospital Admin".
        text "Manage all your patients easily."
    end.
    
    card.
        button "View Patients".
        button "Book Appointment".
    end.

end.
```

When you compile an AAYU file containing a `page`, the internal Compiler synthesizes actual, styled `HTML/CSS` representations into your `views/` directory dynamically.

## Integrating UI with Server

You can map a UI page directly to an HTTP GET route using the `render` command.

```aayu
use http.

get "/dashboard".
    render "Dashboard".
end.

task main.
    serve on 8080.
end.
```

Combined with the `crud Entity.` command, AAYU dynamically generates fully functional data-tables and submission forms in real-time, removing the requirement to write hundreds of lines of React/Vue frontend logic just to see your database values.
