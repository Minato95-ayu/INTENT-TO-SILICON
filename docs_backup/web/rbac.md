# Role-Based Access Control (RBAC)

In traditional frameworks, handling authentication, sessions, and route guards requires heavy middleware and third-party libraries like JWT or Passport.

AAYU eliminates this by baking **Session Management** and **RBAC** directly into the core grammar.

## Defining Roles

You can define user roles natively using the `role` keyword.

```aayu
use rbac.

role Admin.
role Doctor.
role Patient.
```

## Assigning Permissions

Once roles are defined, you can assign explicit CRUD permissions to them via the `allow` keyword.

```aayu
entity Prescription.
    text medication.
end.

# Only the Doctor can create a Prescription
allow Doctor create Prescription.

# A Patient can read a Prescription
allow Patient read Prescription.

# An Admin can do everything
allow Admin read Prescription.
allow Admin delete Prescription.
```

## Guarding Web Routes

When writing custom HTTP routes, you can enforce strict session requirements natively.

```aayu
use auth.

get "/dashboard".
    # This acts as a native middleware. If the user is not logged in, 
    # it immediately halts execution and returns a 401 Unauthorized.
    guard session.
    
    render "Dashboard".
end.
```

The AAYU compiler handles the underlying cryptography (PBKDF2 hashing) and state isolation entirely automatically.
