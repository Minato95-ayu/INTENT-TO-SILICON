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
