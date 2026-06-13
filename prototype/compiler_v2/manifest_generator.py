import yaml

class ManifestGenerator:
    def generate(self, intent, blueprint, concepts):
        """
        Generates an Application Manifest detailing the high-level architecture
        before generating the actual code.
        """
        
        manifest = {
            "app_name": "AayuGeneratedApp",
            "intent": intent,
            "domains": concepts,
            "architecture": {
                "frontend": "react",
                "backend": "fastapi",
                "database": "sqlite_dev_postgres_prod"
            },
            "modules": {
                "frontend": blueprint.get("frontend_modules", []),
                "backend": blueprint.get("backend_modules", [])
            },
            "entities": blueprint.get("data_entities", [])
        }
        
        return yaml.dump(manifest, sort_keys=False)
