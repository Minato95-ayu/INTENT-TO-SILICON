import os
import json
from typing import Dict, Any

class ExpressGenerator:
    """
    Consumes App IR to generate an Express backend.
    """
    def __init__(self, ir: Dict[str, Any], output_dir: str = "backend"):
        self.ir = ir
        self.output_dir = output_dir

    def generate(self):
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "src"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "src", "routes"), exist_ok=True)
        
        project_name = self.ir.get("project", "aayu-express-app").lower().replace(" ", "-")
        
        # package.json
        pkg_json = {
            "name": f"{project_name}-backend",
            "version": "1.0.0",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "dev": "nodemon src/index.js"
            },
            "dependencies": {
                "express": "^4.19.2",
                "cors": "^2.8.5",
                "dotenv": "^16.4.5"
            },
            "devDependencies": {
                "nodemon": "^3.1.4"
            }
        }
        
        with open(os.path.join(self.output_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump(pkg_json, f, indent=2)

        # src/index.js
        index_js = """require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

"""
        api_ir = self.ir.get("api_ir", {})
        services = api_ir.get("services", [])
        
        for service in services:
            service_name = service["name"]
            index_js += f"const {service_name.lower()}Routes = require('./routes/{service_name.lower()}');\n"
            index_js += f"app.use('/api', {service_name.lower()}Routes);\n"
            
            # Generate Route files
            self._generate_route_file(service)

        index_js += """
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
"""
        with open(os.path.join(self.output_dir, "src", "index.js"), "w", encoding="utf-8") as f:
            f.write(index_js)
            
    def _generate_route_file(self, service: Dict[str, Any]):
        route_js = "const express = require('express');\nconst router = express.Router();\n\n"
        
        for endpoint in service.get("endpoints", []):
            method = endpoint["method"].lower()
            path = endpoint["path"]
            # Convert /users/{id} to /users/:id for Express
            import re
            express_path = re.sub(r'\{([^}]+)\}', r':\1', path)
            
            route_js += f"router.{method}('{express_path}', async (req, res) => {{\n"
            route_js += f"    // TODO: Implement {service['name']} {method} {path}\n"
            route_js += "    res.json({ message: 'Not implemented' });\n"
            route_js += "});\n\n"
            
        route_js += "module.exports = router;\n"
        
        with open(os.path.join(self.output_dir, "src", "routes", f"{service['name'].lower()}.js"), "w", encoding="utf-8") as f:
            f.write(route_js)
