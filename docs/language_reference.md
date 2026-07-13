# Language Reference

AAYU is a declarative language. This reference covers the core concepts available in AAYU v1.0.

## 1. Pages
The top-level container for a route.
```aayu
page Home {
    ...
}
```

## 2. State
Reactive variables that trigger UI updates when mutated.
```aayu
state counter = 0
state username = "guest"
```

## 3. Actions
Event handlers containing logic.
```aayu
action login {
    username = "admin"
}
```

## 4. Built-in Widgets
- **container**: A grouping element (like `div`).
- **text**: Renders text on screen. `bind` property binds to state.
- **button**: Clickable element. Uses `onClick` property to bind to an action.
- **input**: Text entry. Uses `bind` property to update state.
- **image**: Displays a picture using the `src` property.
- **heading**: Uses the `level` property for H1-H6.
- **card**: A styled container with elevation.
