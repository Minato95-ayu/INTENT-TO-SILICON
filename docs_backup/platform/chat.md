# AAYU Chat

**Status: Experimental**

AAYU Chat is a conversational AI interface designed to build software architecture, not random code.

## Talk. Design. Generate.

Instead of writing `.aayu` syntax manually, you can tell AAYU Chat what you want to build.

```bash
aayu chat
```

### 1. Cross Question Engine
AAYU Chat doesn't just blindly accept your prompt. It uses a **Data-Driven Question Graph** to ask clarifying questions about your specific domain.

> **AAYU**: "Do you need a Multi-tenant hospital or a Single branch?"
> **AAYU**: "Do patients need a dashboard portal?"

### 2. Intent Engine
Instead of writing raw application code directly, AAYU Chat builds an **Intent Model**. This model represents entities, features, and workflows in the abstract.

### 3. Source Generation
The Intent Model enforces strict translation into valid `.aayu` language syntax. This guarantees that AAYU Chat will **never hallucinate invalid code**. The generated code is always 100% syntactically correct and passed to the Builder API.

## Workflow Example
1. Run `aayu chat`
2. Enter "Hospital"
3. Answer domain-specific questions
4. Review the generated Architecture
5. Accept and auto-generate the full backend and frontend stack.
