# The Intent Engine (v4)

AAYU's crown jewel is its built-in **Native Intent Engine**. AAYU was fundamentally built on the philosophy that human developers should only focus on the **Business Intent**, while the compiler focuses on the **Silicon Execution**.

## Intent to Application

Normally, software engineering requires a long translation pipeline:
`Requirement -> PM -> Systems Architect -> Developer -> Code -> App`

AAYU collapses this entirely.

```bash
aayu build "Build a Police Complaint System"
```

When you type an intent like the one above, the **Native Capability Engine** kicks in. It does not ping external AI APIs (OpenAI/Gemini). It natively reasons through the domain using embedded heuristics to infer business structures.

### 1. Inferred Roles
The Engine identifies who interacts with the system.
```aayu
role Citizen.
role Officer.
role Admin.
```

### 2. Inferred Entities
The Engine extracts what data objects must exist.
```aayu
entity Complaint.
    text description.
end.

entity Evidence.
    text file_path.
end.
```

### 3. Inferred Relations
The Engine constructs the relational database bindings.
```aayu
relation Complaint one_to_many Evidence.
relation Citizen one_to_many Complaint.
```

### 4. Inferred Workflows
The Engine calculates the exact state machine pipeline required for the domain.
```aayu
workflow InvestigationWorkflow for Complaint.
    step Filed.
    step Investigating.
    step Closed.
end.
```

## The Final Output

AAYU automatically writes all of this into a pristine, ready-to-run `main.aayu` file, alongside dynamically generated UI `crud` components.

You go from a single English sentence directly to a full-stack, secure, role-based application in **less than 10 seconds.**

Welcome to the Intent Operating System.
