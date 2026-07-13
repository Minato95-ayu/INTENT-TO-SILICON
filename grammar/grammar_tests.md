# Grammar v1.0 Tests

The following syntax is officially supported and frozen for AAYU v1.0.

## 1. App Configuration
```aayu
app MyService.
server Port3000.
storage CloudDB.
```

## 2. Models
```aayu
model Product {
    id Int.
    price Number.
    tags String[].
}
```

## 3. Tasks and Basic Logic
```aayu
task process(a, b) {
    let result = a + b.
    return result.
}
```

## 4. Control Flow
```aayu
task check(x) {
    if (x > 10) {
        show "Large".
    } else {
        show "Small".
    }
}
```

## 5. Storage Operations
```aayu
task db_test {
    insert Product {
        price = 99.99.
    }.
    
    let products = find Product.
    
    update Product {
        price = 49.99.
    }.
    
    delete Product.
}
```

## 6. Error Handling
```aayu
task safe_div(a, b) {
    try {
        return a / b.
    } catch {
        show "Division error".
    } finally {
        show "Cleanup".
    }
}
```
