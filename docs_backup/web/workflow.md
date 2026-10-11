# Workflow Engine

Modern business applications are rarely just CRUD tables. A `Lead` becomes an `Opportunity` and then a `Customer`. A `Prescription` gets `Prescribed` and then `Dispensed`. 

AAYU ships with a built-in State Machine via the `workflow` keyword, allowing you to track linear entity lifecycles effortlessly.

## Defining a Workflow

You define a workflow by attaching it to an existing `entity`.

```aayu
use workflow.

entity Order.
    text item.
end.

workflow OrderWorkflow for Order.
    step Pending.
    step Paid.
    step Shipped.
    step Delivered.
end.
```

## How It Works Natively

When the AAYU Compiler encounters a `workflow` block, it automatically:
1. Provisions the state graph logic internally.
2. Registers a hidden state tracking column to the entity inside SQLite.
3. Automatically maps the linear transition constraints so an `Order` cannot jump directly from `Pending` to `Delivered`.

With just 6 lines of code, you have a mathematically rigorous State Machine integrated into your database.
