# Standard Library

AAYU is an opinionated language designed for building software platforms. Instead of forcing developers to download hundreds of third-party dependencies for standard application features, AAYU includes a robust Standard Library baked into the runtime.

Modules are imported using the `use` keyword.

```aayu
use http.
use db.
use auth.
```

## `db` Module
Handles all database interactions. In AAYU, you rarely write raw SQL. The `db` module interacts directly with your declared `entity` definitions.

- `create [Entity] with [Map]`
- `find [Entity]`
- `update [Entity] where [Condition] with [Map]`
- `delete [Entity] where [Condition]`

*(Note: These are syntax-level built-ins rather than traditional function calls to optimize the DX).*

## `http` Module
Handles web server routing and requests.

### Routing
Routes map URL paths to AAYU tasks.
```aayu
get "/api/users" to fetch_users.
post "/api/users" to create_user.
```

### Request Context
The `http` module automatically injects context into route handler tasks.
- `form "field" from req`: Extracts form data.
- `path "id" from req`: Extracts URL path parameters.
- `json req`: Parses the request body as a JSON map.

### Server Lifecycle
- `serve on [Port]`: Starts the HTTP server.

## `auth` and `rbac` Modules
Handle identity and access control natively.

```aayu
use rbac.

role Admin.
role Manager.

allow Admin create User.
allow Manager update Document.
```

## Future Extensions

The AAYU Standard Library is designed to expand based on the Intent Engine ecosystem. Future built-in modules will include:

- **`vision`**: Native image processing and AI OCR.
- **`dataframe`**: Native data manipulation (pandas-equivalent).
- **`rag`**: Built-in vector database and Retrieval-Augmented Generation capabilities.
