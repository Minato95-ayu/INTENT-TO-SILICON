# Relations

Data modeling in modern applications is heavily dependent on how entities relate to one another. AAYU provides a declarative syntax for defining relationships between entities, which the compiler uses to automatically generate database foreign keys, join tables, and ORM configurations.

## The `relation` Keyword

Relations are declared outside of `entity` blocks using the `relation` keyword. The syntax reads like a natural language sentence:

`relation [SourceEntity] [relation_type] [TargetEntity].`

## Supported Relation Types

### `one_to_many`
A single record in the Source Entity can be associated with multiple records in the Target Entity.

```aayu
entity Department.
    text name.
end.

entity Employee.
    text full_name.
end.

# One Department has many Employees
relation Department one_to_many Employee.
```
*Compiler Action:* In a relational database target, the compiler will automatically add a `department_id` foreign key column to the `Employee` table.

### `one_to_one`
A strict 1:1 mapping between two entities.

```aayu
entity User.
    text username.
end.

entity UserProfile.
    text bio.
    text avatar_url.
end.

relation User one_to_one UserProfile.
```
*Compiler Action:* The compiler creates a foreign key with a unique constraint, ensuring the 1:1 nature of the relationship.

### `many_to_many`
Records in the Source Entity can belong to multiple records in the Target Entity, and vice-versa.

```aayu
entity Student.
    text name.
end.

entity Course.
    text title.
end.

relation Student many_to_many Course.
```
*Compiler Action:* The compiler will automatically generate a hidden join table (e.g., `student_course`) to manage the associations.

## Querying Relations

While current AAYU prototypes handle querying via standard `find` operations on the child entities (filtering by the injected foreign keys like `department_id`), future versions of the specification will include deep-nested retrieval syntax natively (e.g., `find Department with Employees`).
