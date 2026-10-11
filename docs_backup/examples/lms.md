# Building an LMS (Learning Management System)

AAYU shines when building complex, domain-specific architectures thanks to the Intent Engine.

## The AAYU Way

Open your terminal and run:

```bash
aayu build "Build a College LMS"
```

### What Happens Under the Hood?

1. **Domain Recognition**: AAYU recognizes the "College LMS" domain.
2. **Clarification**: AAYU might ask if you want "Online Payments" or "Automated Grading".
3. **Architecture Generation**: AAYU automatically infers the relational architecture.
   - It sees `Student` and `Course` and automatically creates an `Enrollment` junction table (M:N relationship).
   - Because a College LMS implies user login, AAYU automatically injects `User`, `Role`, and `Permission` entities for RBAC (Role-Based Access Control).
4. **Code Emission**: It generates a fully valid `main.aayu` handling all HTTP routing to dashboard pages.
5. **UI Generation**: It emits dynamic, domain-specific HTML templates in `views/` with styled Tailwind-like CSS, showing real-time mockup data tables for Students and Courses!

With AAYU, you skip the boilerplate and start iterating on business logic on day one.
