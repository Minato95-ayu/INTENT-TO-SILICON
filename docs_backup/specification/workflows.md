# Workflows & State Machines

Many business applications require tracking the state of an entity over time (e.g., an Order moving from *Pending* to *Shipped* to *Delivered*). Traditionally, this involves writing complex boolean flags or status enum checks scattered throughout the codebase.

AAYU elevates this concept to a first-class citizen using the `workflow` block, creating a rigid, compiler-enforced state machine attached to an entity.

## Defining a Workflow

A workflow is defined using the `workflow` keyword, named, and explicitly attached to a specific `entity` using the `for` keyword.

Inside the workflow block, the `step` keyword defines the valid sequential states.

```aayu
entity Order.
    text customer_name.
    number total.
end.

workflow OrderFulfillment for Order.
    step Pending.
    step Processing.
    step Shipped.
    step Delivered.
    step Cancelled.
end.
```

## Compiler Actions

When the AAYU Compiler encounters a `workflow`:

1.  **Schema Update**: It automatically injects a `status` field into the target `entity` (e.g., `Order.status`).
2.  **Default State**: It sets the default value of new records to the *first* defined step (e.g., `Pending`).
3.  **Validation**: It generates runtime guardrails ensuring that state transitions occur in a valid order (e.g., you cannot move from `Pending` directly to `Delivered` without custom override logic, and you cannot assign a status that doesn't exist in the workflow).

## Future Capabilities

Future revisions of the AAYU specification will introduce transition hooks:

```aayu
# Proposed future syntax
on transition from Processing to Shipped.
    run send_shipping_email with order.
end.
```
