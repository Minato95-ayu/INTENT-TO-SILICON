# Entity Relations

In modern applications, entities rarely exist in isolation. AAYU allows you to link entities together natively using the `relation` keyword, completely removing the need for raw SQL JOINs.

AAYU automatically configures foreign keys and handles cascading logic at the compiler level.

## One-to-Many

The most common relationship. For example, a single `Doctor` can have multiple `Appointment`s.

```aayu
use db.

entity Doctor.
    text name.
end.

entity Appointment.
    text date.
end.

# AAYU handles the foreign key injection automatically
relation Doctor one_to_many Appointment.
```

## Many-to-Many

For complex systems, such as a Learning Management System where a `Student` can enroll in multiple `Course`s, and a `Course` can have multiple `Student`s.

```aayu
entity Student.
    text name.
end.

entity Course.
    text title.
end.

# AAYU handles the underlying junction architecture natively
relation Student many_to_many Course.
```

## Supported Relation Types

- `one_to_one`
- `one_to_many`
- `many_to_one`
- `many_to_many`

By defining these relations natively, AAYU's Intent Engine is able to construct deep, generalized business systems instantly.
