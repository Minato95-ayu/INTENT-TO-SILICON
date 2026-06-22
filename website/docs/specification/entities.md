# Entities & Data Models

In AAYU, the `entity` block is the fundamental building block for data modeling. An `entity` represents a discrete business object, mapping directly to a database table or a document collection in the generated backend.

## Defining an Entity

An entity is declared using the `entity` keyword, followed by its name (PascalCase is recommended) and a period. Inside the entity block, properties are declared using their type and name.

```aayu
entity User.
    text username.
    text email.
    boolean is_active.
end.
```

## Automatic Properties

By default, the AAYU compiler automatically provisions standard tracking fields for every entity:
- `id`: A unique primary key (auto-incrementing integer or UUID depending on the target engine).
- `created_at`: The timestamp when the record was created.

*Note: In future versions of the specification, the `id` type behavior will be configurable globally or per-entity.*

## Using Entities in Code

Once an entity is defined, the AAYU Standard Library (`db` module) provides built-in functions to interact with it.

### Creating Records
```aayu
map new_user.
set "username" to "alice" in new_user.
set "email" to "alice@example.com" in new_user.

create User with new_user.
```

### Finding Records
```aayu
# Retrieve all users
list all_users is find User.

# Retrieve a specific user
list admins is find User where "is_active" equal to true.
```

### Updating Records
```aayu
map update_data.
set "is_active" to false in update_data.

update User where "username" equal to "alice" with update_data.
```

### Deleting Records
```aayu
delete User where "username" equal to "alice".
```
