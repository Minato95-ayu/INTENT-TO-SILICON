# Data Types

AAYU provides a set of strong, built-in data types tailored for building modern software applications.

## Primitive Types

### `text`
Represents a string of characters. Text literals are enclosed in double quotes.
```aayu
text name is "AAYU Developer".
```

### `number`
Represents numeric values. AAYU's `number` type handles both integers and floating-point values seamlessly.
```aayu
number count is 10.
number price is 19.99.
```

### `boolean`
Represents a truth value, either `true` or `false`.
```aayu
boolean is_admin is true.
```

## Collection Types

### `list`
An ordered collection of items. Lists can contain items of mixed types, though homogenous lists are recommended.
```aayu
list tags is ["urgent", "backend", "v1"].
```
You can access list items using the `at` keyword (0-indexed).
```aayu
text first_tag is tags at 0.
```

### `map`
A key-value data structure, equivalent to an object in JSON or a dictionary in Python.
```aayu
map user_data.
set "username" to "alice" in user_data.
set "role" to "admin" in user_data.
```
Values can be retrieved using the `get` keyword.
```aayu
text username is get "username" from user_data.
```

## Future Type Extensions

As the AAYU specification evolves, the following types are planned for native integration to support robust database and API modeling:

- `uuid`: A universally unique identifier.
- `date` / `datetime`: Native representations of time and duration.
- `email`: A validated email string type.
- `file`: A representation of uploaded binary data.
