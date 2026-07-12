# AAYU Language Reference

The AAYU language is designed to be the ultimate operating system for the next generation of applications. This reference covers the keywords, types, and standard library available in AAYU.

## Keywords

- `state`: Declares a globally reactive state variable. Changes to this variable automatically trigger reactive updates in the UI and connected systems.
- `page`: Defines a UI root node. Represents a full screen or web page.
- `layout`: Defines a layout container (e.g., column, row, grid) for widgets.
- `text`: Defines a text widget for displaying strings.
- `button`: Defines an interactive button widget.
- `input`: Defines a text input widget. Supports `bind:` to directly tie its value to a `state`.
- `fn`: Defines a function.
- `if` / `else`: Conditional branching.
- `for` / `in`: Loops over collections.
- `model`: Defines a data model (Entity) for the Storage Runtime.
- `end`: Terminates a block (e.g., `fn`, `model`, `page`, `if`, `for`).

## Standard Library Functions

### Collections
- `collection_len(coll)`: Returns the length of a list or map.

### Strings
- `string_contains(s, sub)`: Returns 1.0 if `sub` is in `s`, else 0.0.

### Database / Storage
- `db_register_entity(name, fields)`: Registers a model schema in SQLite.
- `db_register_relation(entity1, rel_type, entity2)`: Registers a relation.
- `db_create(entity, data)`: Inserts a record.
- `db_find(entity, field, value)`: Finds records.
- `db_update(entity, field, value, data)`: Updates records.
- `db_delete(entity, field, value)`: Deletes records.

### Network & HTTP
- `http_serve(port, handler_name)`: Starts an HTTP server on `port` using the given root handler.
- `http_route(path, method, handler)`: Registers an HTTP route handler.
- `http_request(options)`: Makes an outbound HTTP request.
- `json_serialize(data)`: Converts a map/list to a JSON response object.

### Authentication
- `auth_create_account(data)`: Creates a new user account with hashed password.
- `auth_login(data)`: Authenticates user and sets session cookie.
- `auth_logout(req)`: Logs out and clears session.
- `auth_guard_session()`: Verifies session validity; returns account ID or raises unauthorized error.
