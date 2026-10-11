# AAYU Runtime Architecture

AAYU implements a Microkernel OS architecture to decouple compilation from execution and easily support diverse environments (CLI, Web, Native).

## The Kernel (`RuntimeKernel`)

The Kernel is the central message bus and plugin registry. It handles dispatching instructions from the Virtual Machine (VM) to the appropriate runtime plugin.

- **`dispatch(target, action, payload)`**: The primary interface for inter-plugin communication and VM-to-OS communication.
- **EventBus**: Supports Pub/Sub events across the entire application ecosystem.

## Runtime Plugins

AAYU runs on a series of interchangeable plugins.

### 1. Scheduler Runtime (`scheduler`)
- Prioritizes tasks.
- Handles `tick()` based delayed execution without busy-waiting.
- In Phase 2, built on `threading` and `queue`.

### 2. Event Runtime (`events`)
- Global Event Bus.
- Manages pub/sub subscriptions for UI updates and inter-process communication.

### 3. Network Runtime (`network`)
- Handles outbound `http_request`.
- Manages sockets and timeouts.

### 4. Web Runtime (`web`)
- Handles inbound HTTP traffic.
- Executes `http_serve` and routes.
- Maps endpoints to AAYU functions.

### 5. Storage Runtime (`storage`)
- Manages persistent data.
- Handles `insert`, `query`, `update`, `delete`.
- Uses SQLite backend by default (with WAL support).
- Supports transactions.

### 6. State Runtime (`state`)
- In-memory reactive state manager.
- Supports `snapshot` and `restore` for time-travel debugging.
- Watches fields and emits events to trigger the UI Runtime.

### 7. UI Runtime (`ui`)
- Parses AAYU Widget AST into a Logical UI Tree.
- Computes what widgets need to be updated (Dependency Graph) instead of full re-renders.

### 8. Render Runtime (`render`)
- Takes the Logical UI Tree and renders it to a specific target (Terminal, Web DOM, or Native).
- Includes the Diff Engine to calculate minimal patch sets.

### 9. Theme Runtime (`theme`)
- Manages global aesthetics, colors, and layout tokens.
