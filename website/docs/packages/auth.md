# aayu-auth

The `aayu-auth` package provides native, secure authentication capabilities for AAYU.

## Functions

- `auth.create_account(email, password)`: Creates an account.
- `auth.login(email, password)`: Logs the user in and starts a secure session.
- `auth.logout()`: Ends the current session.
- `auth.guard_session(req)`: Middleware to check if the session is valid, returns boolean.
