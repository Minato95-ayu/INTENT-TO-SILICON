import os
from typing import Dict, Any

class HtmlGenerator:
    """
    Consumes UI IR and generates a vanilla HTML/CSS/JS application.
    """
    def __init__(self, ir: Dict[str, Any], output_dir: str = "dist"):
        self.ir = ir
        self.output_dir = output_dir

    def generate(self):
        os.makedirs(self.output_dir, exist_ok=True)
        
        project_name = self.ir.get("project", "AAYU App")
        
        html_content = [
            f"<!DOCTYPE html>",
            f"<html lang='en'>",
            f"<head>",
            f"    <meta charset='UTF-8'>",
            f"    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"    <title>{project_name}</title>",
            f"    <link rel='stylesheet' href='style.css'>",
            f"</head>",
            f"<body>",
            f"    <div id='app'>"
        ]
        
        for page in self.ir.get("pages", []):
            html_content.append(f"        <div class='page' id='page-{page['name'].lower()}'>")
            for comp in page.get("components", []):
                if comp["type"] == "title":
                    html_content.append(f"            <h1>{comp['text']}</h1>")
                elif comp["type"] == "button":
                    html_content.append(f"            <button>{comp['text']}</button>")
            html_content.append(f"        </div>")
            
        html_content.append("    </div>")
        html_content.append("    <script src='app.js'></script>")
        html_content.append("</body>")
        html_content.append("</html>")
        
        with open(os.path.join(self.output_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write("\n".join(html_content))
            
        with open(os.path.join(self.output_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write("body { font-family: sans-serif; padding: 2rem; }\nbutton { padding: 10px 20px; cursor: pointer; }\n")
            
        with open(os.path.join(self.output_dir, "app.js"), "w", encoding="utf-8") as f:
            f.write(f"console.log('{project_name} initialized');\n")
            
        print(f"[HTML Generator] Generated project '{project_name}' in '{self.output_dir}'")
