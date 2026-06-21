# Database Models

AAYU abstracts the database layer so you can define tables naturally. The default database engine is SQLite.

```aayu
use db.

entity Book.
    text title.
    text author.
    number year_published.
end.

# Querying the database
task get_books.
    return db_find("Book", {}).
end.
```
