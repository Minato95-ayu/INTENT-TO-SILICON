# AAYU 30-Second Demo Script

This script is designed for maximum visual impact to demonstrate AAYU's "Intent to Silicon" capabilities instantly.
Target length: 30-45 seconds. Keep pacing fast!

## Scene 1: The Setup (0-5s)
**Visual**: An empty VS Code window. The AAYU extension is visibly active (showing the purple AAYU icon at the bottom).
**Action**: You open a terminal at the bottom.
**Voiceover / Caption**: "Want to build a full-stack Job Portal?"

## Scene 2: The Intent (5-15s)
**Visual**: The terminal window.
**Action**: Type the magical command:
```bash
$ aayu build "Build a Job Portal"
```
**Visual**: The CLI instantly parses the domain and asks the clarification questions:
```text
System: Do you need user authentication? (y/n)
[You type 'y' and hit enter]
System: Will this handle resume uploads? (y/n)
[You type 'n' and hit enter]
```
**Voiceover / Caption**: "Just tell AAYU what you want. It infers the architecture automatically."

## Scene 3: The Generation (15-25s)
**Visual**: The terminal logs flying by as AAYU generates the code.
```text
[3/3] Emitting Full Stack AAYU Code...
✔ Generated main.aayu
✔ Generated database schema (Candidate, Job, Company, JobApplication)
✔ Generated views/dashboard.html
✔ Generated views/jobs.html
```
**Action**: You quickly click on `main.aayu` to show the beautiful, human-readable code. You click on `views/dashboard.html` to show the generated UI.
**Voiceover / Caption**: "It generates the database, backend routes, and frontend templates in seconds."

## Scene 4: The Result (25-35s)
**Visual**: Split screen. Terminal on the left showing `Server running at http://localhost:8080`, and a web browser on the right.
**Action**: You refresh the browser at `localhost:8080`.
The beautiful styled Job Portal UI appears! It shows the Navigation Bar, Login button, and mock data tables for `Recent Candidates` and `Recent Jobs`.
**Voiceover / Caption**: "AAYU: The world's first Intent-to-Silicon language."
