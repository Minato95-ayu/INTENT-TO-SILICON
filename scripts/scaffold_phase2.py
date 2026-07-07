import os

brainos_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\brainos"

def write_file(path, content):
    full_path = os.path.join(brainos_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

write_file("production_review.py", """\
class ProductionReview:
    def evaluate(self, architecture_plan: dict) -> dict:
        return {
            "status": "Production-Ready",
            "checklist": ["Load Balancing", "Monitoring", "Logging", "Database Backups"],
            "score": 95
        }
""")

write_file("folder_generator.py", """\
import os
import json

class FolderGenerator:
    def generate(self, base_path: str, structure: dict):
        for item in structure.get('folders', []):
            os.makedirs(os.path.join(base_path, item), exist_ok=True)
        return {"status": "success", "base_path": base_path}
""")

write_file("dependency_generator.py", """\
class DependencyGenerator:
    def resolve_dependencies(self, architecture: dict) -> dict:
        tech_stack = architecture.get('technologies', [])
        deps = {}
        for tech in tech_stack:
            if tech == "react":
                deps["react"] = "^18.2.0"
                deps["react-dom"] = "^18.2.0"
            elif tech == "fastapi":
                deps["fastapi"] = "^0.100.0"
                deps["uvicorn"] = "^0.23.0"
        return deps
""")

write_file("multi_file_generator.py", """\
import os

class MultiFileGenerator:
    def write_files(self, base_path: str, files: dict):
        results = []
        for file_path, content in files.items():
            full_path = os.path.join(base_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            results.append(full_path)
        return results
""")

write_file("technology_selector.py", """\
class TechnologySelector:
    def select(self, requirements: list) -> dict:
        tech = []
        if "frontend" in requirements:
            tech.append("react")
        if "backend" in requirements:
            tech.append("fastapi")
        if "database" in requirements:
            tech.append("postgresql")
        return {"selected": tech}
""")

write_file("scaling_advisor.py", """\
class ScalingAdvisor:
    def advise(self, load_params: dict) -> dict:
        req_per_sec = load_params.get("requests_per_second", 0)
        if req_per_sec > 10000:
            return {"strategy": "microservices", "database": "sharded", "cache": "redis cluster"}
        elif req_per_sec > 1000:
            return {"strategy": "load_balanced_monolith", "database": "primary_replica", "cache": "redis"}
        else:
            return {"strategy": "monolith", "database": "single", "cache": "in-memory"}
""")

print("Phase 2 scaffolding complete")
