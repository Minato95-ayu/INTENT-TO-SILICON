# Hello World

AAYU makes UI development declarative and state-driven. Let's look at a simple Hello World app.

```aayu
page Home {
    state counter = 0

    action increment {
        counter = counter + 1
    }

    container {
        text { "Hello AAYU World!" }
        text { "Counter: " + counter }
        button {
            text "Increment"
            onClick increment
        }
    }
}
```

## Structure
- **page**: Represents a full-screen view or route.
- **state**: Declares a reactive variable. When it changes, the UI updates automatically.
- **action**: A block of logic bound to UI events.
- **container, text, button**: Built-in UI widgets.