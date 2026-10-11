# AAYU Language Guide (5-Minute Read)

Welcome to AAYU! The `.aayu` language is designed to be highly readable and extremely fast to write. Think of it as a blueprint for your entire software architecture.

Every statement in AAYU ends with a period `.`.
Blocks are closed with the `end.` keyword.

---

## 1. Modules

Tell AAYU which systems your application needs. For a web application, you typically want a database and a web server:

```aayu
use db.
use http.
```

---

## 2. Entities

Entities define your data models (database tables).

```aayu
entity Doctor.
    text name.
    text specialization.
    number experience.
end.
```

**Supported field types:**
- `text`
- `number`
- `boolean`
- `date`

---

## 3. Relations

You don't need to manually write Foreign Keys or Join Tables! AAYU infers them based on plain-english relationships.

```aayu
relation Doctor one_to_many Patient.
relation Patient many_to_many Appointment.
```

**Supported relations:**
- `one_to_one`
- `one_to_many`
- `many_to_one`
- `many_to_many`

---

## 4. Workflows & Tasks

Define backend business logic. A `task` is a function, and a `workflow` chains multiple tasks together.

```aayu
task register_patient with data.
    return "Patient Registered!".
end.

workflow OnboardPatient.
    step register_patient.
end.
```

---

## 5. Routes

Expose your tasks via HTTP endpoints. 

```aayu
post "/api/patients/register" to register_patient.
get "/api/patients" to get_all_patients.
```

---

## 6. Pages (UI)

Define which pages should exist in your frontend application.

```aayu
page Dashboard.
end.

page PatientProfile.
end.
```

---

### Full Example

```aayu
use http.
use db.

entity Author.
    text name.
end.

entity Post.
    text title.
    text content.
end.

relation Author one_to_many Post.

task publish_post with data.
    return "Success".
end.

post "/api/posts/publish" to publish_post.

page Dashboard.
end.
```
