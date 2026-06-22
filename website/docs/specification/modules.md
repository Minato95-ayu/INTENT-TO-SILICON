# Modules & Packages

AAYU supports a clean, hierarchical module system to organize large applications.

## The `use` Keyword

The `use` keyword is used to import functionality from the standard library or from other AAYU packages within your project workspace.

```aayu
use http.
use db.
```

## Packages

In AAYU, a package is simply a directory containing `.aayu` files. The compiler treats the entire directory as a single module namespace.

*More details on custom package authoring and the AAYU Package Manager (APM) will be provided in future revisions of this specification.*
