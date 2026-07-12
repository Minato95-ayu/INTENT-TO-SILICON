# Pages & UI DSL

A core feature of the AAYU platform is its ability to not just generate backend APIs, but full-stack applications. To achieve this, AAYU includes a declarative Domain-Specific Language (DSL) for defining user interfaces.

The UI DSL allows developers to outline the structure and components of a frontend without writing HTML, CSS, or React directly.

## The `page` Block

A UI view is defined using the `page` keyword.

```aayu
page LoginView.
    heading "Welcome to AAYU".
    button "Login".
end.
```

## Layout Components

AAYU provides semantic layout components to structure the page.

### `dashboard`
The `dashboard` component automatically provisions a standard administrative layout (typically a sidebar on the left and a main content area on the right).

```aayu
page AdminArea.
    dashboard.
        # Sidebar goes here
        # Main content goes here
    end.
end.
```

### `sidebar` and `column`
Used within a `dashboard` or page to organize content vertically.

```aayu
page CRM.
    dashboard.
        sidebar.
            text "Leads".
            text "Customers".
            text "Settings".
        end.
        column.
            heading "Dashboard Overview".
            text "Welcome back, Admin.".
        end.
    end.
end.
```

## Data Integration Components

### `table`
The `table` component seamlessly integrates with AAYU `entity` definitions to automatically generate data grids.

```aayu
entity Patient.
    text name.
end.

page PatientList.
    column.
        heading "All Patients".
        table "Patients" from Patient.
    end.
end.
```
*Compiler Action:* The compiler will generate the necessary frontend code (e.g., a React component) to fetch `Patient` data from the backend and render it in a tabular format.

### `form` and `input`
Used to capture user input.

```aayu
page AddLead.
    form.
        input "Company Name" to lead_company.
        input "Contact Email" to lead_email.
        button "Save Lead".
    end.
end.
```

## Rendering Pages

Pages are rendered from within `task` blocks (route handlers) using the `render` keyword.

```aayu
task show_dashboard with req.
    return render "CRM.html".
end.

get "/dashboard" to show_dashboard.
```
*(Note: Current prototype targets generate `.html` strings natively. Future Target Generators will emit React/Vue router code based on these declarations).*
