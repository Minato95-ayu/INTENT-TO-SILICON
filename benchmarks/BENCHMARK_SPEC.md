# AAYU Web Backend Benchmark v1.0

## 1. Overview
This benchmark evaluates the performance, resource footprint, and developer experience of the AAYU compiler and runtime compared to industry-standard Python frameworks (FastAPI and Django). The benchmark forces all frameworks to implement an identical feature matrix to ensure a mathematically fair comparison of framework overhead.

## 2. Hardware and Environment
- **CPU**: (To be recorded at runtime)
- **RAM**: (To be recorded at runtime)
- **OS**: Windows (Target Platform)
- **Python Version**: >= 3.11
- **Database**: SQLite (Local)

## 3. Scenario & Feature Matrix
All frameworks must implement the following functionality exactly:
- **SQLite Database** with a standard `Product` and `Order` schema.
- **CRUD Endpoints**: `GET /products`, `POST /products`.
- **Health Check**: `GET /health` (For pure framework routing overhead).
- **Authentication**: JWT token generation and validation.
- **Validation**: Payload schema validation.
- **Documentation**: OpenAPI generation.

| Feature    | AAYU | FastAPI | Django |
| ---------- | ---- | ------- | ------ |
| SQLite     | ✅    | ✅       | ✅      |
| JWT        | ✅    | ✅       | ✅      |
| CRUD       | ✅    | ✅       | ✅      |
| Validation | ✅    | ✅       | ✅      |
| OpenAPI    | ✅    | ✅       | ✅      |

## 4. Workload Specification
The load test is performed using a custom Python `asyncio` harness, optionally validated with an external tool (e.g., `oha`).

- **Warm-up Phase**: 100 requests to initialize JIT, connections, and cache.
- **Measurement Phase**:
  - 10,000 `GET /health` requests
  - 10,000 `GET /products` requests
  - 10,000 `POST /products` requests

## 5. Metrics Collected

### Developer Experience (DX)
- **LOC (Lines of Code)**: Total lines required to build the feature matrix.
- **Files**: Number of files required.
- **Dependency Count**: Number of external libraries.
- **Dependency Size**: Total size (MB) of the required virtual environment.

### Runtime Metrics
- **Startup Time (ms)**: Time taken from command invocation to port binding.
- **Idle RAM (MB)**: Memory footprint after startup but before traffic.
- **Peak RAM (MB)**: Maximum memory footprint during the load test.
- **CPU Usage (%)**: Peak CPU utilization.

### HTTP Performance
- **RPS (Requests Per Second)**: For GET and POST separately.
- **Latency**: P50, P95, and P99 percentiles.

### Build Metrics
- **Build Time**: Only applicable to AAYU (compilation time).
- **Binary / Project Size**: Disk footprint of the application.

## 6. Threats to Validity
To ensure reviewer-proof results, we control for the following variables:
- **Same Hardware & OS**: All tests execute on the same machine.
- **Same SQLite Implementation**: Database bottlenecks are equalized; differences reflect framework ORM/I/O layers.
- **Same Schema & JSON**: Payload serialization/deserialization load is perfectly matched.
- **Same Authentication**: JWT algorithms and token sizes are identical.
- **Deterministic Measurement**: A strictly single-threaded, isolated benchmark runner orchestrates the start, warm-up, measure, and teardown cycles without manual intervention.
