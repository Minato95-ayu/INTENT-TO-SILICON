# AAYU Master Recovery Plan

Based on the deep audit, we are going to fix AAYU systematically, prioritizing reality over mock claims, and focusing entirely on the AAYU ecosystem rather than Python scripts.

## Phase 1: Website UI & Playground Reality Check (Immediate)
- **Frontend Restoration**: Restore the hero section UI, benchmarks, download button, and founder details exactly as they were, ensuring the "AI Agent side-by-side with running code" UI is flawless. 
- **Playground API Connect**: 
  - Stop mocking output with 800ms timeouts. Connect the Run button to the actual compiler API.
  - Show real lexer, parser, bytecode, and execution results.
- **Security Check**: Remove Gemini API calls from the browser frontend. The API key and LLM integration must happen securely on the backend (`api/main.py`).
- **Fix Broken Links**: Stop Docs from rendering in Tutorial. Fix the Footer Blog links.
- **Benchmark Honesty**: Replace hardcoded generic benchmarks with actual reproducible metrics (e.g., Fibonacci, file I/O) running via the AAYU VM. Include hardware/methodology details.

## Phase 2: Repository Hygiene (Immediate)
- **Clean Git Tracking**: I have already removed `website/node_modules`, `website/.venv`, and `eslint_report.json` from the repository tracking.
- **Delete Python Scratch Scripts**: I have deleted `fix_*.py` and other internal debug scripts. We will no longer clutter the repo with Python debugging tools.

## Phase 3: Making Official Packages & Modules "AAYU-First"
- We currently have 15 official packages (e.g., `aayu-fs`, `aayu-http`, `aayu-math`, `aayu-gemini`), but 13 of them fail to compile because they use outdated syntax or C-style wrappers.
- **Action**: Rewrite the `main.aayu` files for all 15 official packages using the **self-hosted compiler grammar**. Ensure they compile and execute flawlessly under `src/self_hosted/aayuc.aayu`.
- **Package Registry**: Implement the basic GitHub registry fetch mechanism in the package manager so `aayu install` actually downloads and sets up packages, instead of throwing `PackageNotFoundError`.

## Phase 4: Fixing Server, DB & AAYUGram Integration
- The web server integration and database models currently have bugs when handling realistic apps like AAYUGram.
- **Action**: Debug and resolve the `ValueStack underflow` and `TypeError` issues in state scopes, ensuring AAYUGram runs perfectly locally on port 8080.
- **Action**: Implement basic HTTPS/SSL capabilities in the server module.

## Phase 5: Self-Hosted Compiler Maturation
- Stop using Python CLI tools (`tools/cli.py`) for everything!
- Make `src/self_hosted/aayuc.aayu` the primary executable we use to run, build, and test AAYU code. We must eat our own dog food to prove self-hosting works.
