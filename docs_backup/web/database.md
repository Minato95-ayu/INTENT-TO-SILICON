# Database Entities

AAYU comes with native, thread-safe SQLite integration baked directly into the language. You do not need Prisma, TypeORM, or raw SQL queries to persist data.

## Declaring Entities

An `entity` in AAYU maps directly to a relational database table.

```aayu
use db.

entity Product.
    text name.
    number price.
    boolean in_stock.
end.
```

When AAYU compiles this code, it automatically generates a SQLite database, handles the migrations, and ensures the table `Product` exists with the correct column types (`TEXT`, `REAL`, `INTEGER`).

## Database Operations

AAYU provides built-in database keywords to interact with your entities seamlessly:

### Creating Records
```aayu
create Product "name" "Laptop" "price" 1200 "in_stock" true.
```

### Finding Records
```aayu
map product_data.
find Product 1 into product_data.

print product_data["name"].
```

### Fetching All Records
```aayu
map all_products.
find_all Product into all_products.
```

### Updating Records
```aayu
update Product 1 "price" 999.
```

### Deleting Records
```aayu
delete Product 1.
```

All interactions use an underlying Write-Ahead Log (WAL) architecture to ensure maximum concurrency when accessed from the web server.
