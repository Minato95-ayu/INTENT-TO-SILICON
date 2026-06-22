<div align="center">
  <img src="https://via.placeholder.com/1000x300?text=AAYU+Architecture" alt="AAYU Ecosystem Overview">
</div>

# AAYU

**AAYU is an Architecture-First Software Factory that transforms business intent into production-ready software.**

Describe your business system.
Generate a complete React + FastAPI + PostgreSQL application.
Own the code. Modify the code. Deploy the code.

---

## 10-Minute Onboarding: What is AAYU?

AAYU handles the heavy lifting of software architecture. Instead of spending days writing database schemas, REST APIs, and React boilerplate, you define your **Intent** in a simple `.aayu` file, and AAYU builds the factory for you.

### Two Ways To Use AAYU

**1. Describe Intent (The Natural Way)**
You describe the core entities and relationships of your business:
*e.g. "I need a Hospital Management System with Doctors, Patients, and Appointments."*
AAYU maps this to a formalized schema.

**2. Write AAYU (The Developer Way)**
You write a clean `.aayu` file directly:
```aayu
use db.
use http.

entity Doctor.
    text name.
    text specialization.
end.

entity Patient.
    text name.
end.

relation Doctor one_to_many Patient.
```

### The Output

Run `aayu generate` and AAYU deterministically creates:
- **Frontend:** A Vite + React web app ready for UI components.
- **Backend:** A FastAPI python server with CRUD endpoints and Pydantic models.
- **Database:** A PostgreSQL schema with automatically injected foreign keys and many-to-many join tables.
- **Orchestration:** A `docker-compose.yml` to spin the entire stack up in one command.

---

## Quick Start

### 1. Installation
Clone the repository and verify your system:
```bash
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON

# Check if you have Node, Python, and Docker installed
python prototype/cli.py doctor
```

### 2. Initialize a Project
Create a new AAYU project scaffolding:
```bash
python prototype/cli.py init my_hospital
cd my_hospital
```
*(This will generate a `src/main.aayu` file. Need help writing syntax? Check out the [Language Guide](docs/LANGUAGE_GUIDE.md).)*

### 3. Generate Your App
Once your `main.aayu` is ready, compile your intent into silicon:
```bash
python ../prototype/cli.py generate src/main.aayu
```

### 4. Run the Generated Output
AAYU automatically creates a `generated/` directory complete with instructions.
```bash
cd generated
docker-compose up --build
```
Your full-stack application is now live at `http://localhost:3000`!

---

## Philosophy: Intent vs Code

AAYU scaffolds **90%** of the boilerplate, database wiring, and architecture. You write manual code for the remaining **10%** (custom business logic, complex UI components, third-party integrations). AAYU gives you total ownership of the generated code—it is not a black box, it is a launchpad.
