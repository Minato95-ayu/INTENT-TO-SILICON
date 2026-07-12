"""
=============================================================================
FILE: ui_generator.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from compiler.frontend.ast_nodes import UIPageNode, UIComponentNode, UIElementNode, TextNode, VariableNode
import os

class UIGenerator:
    def __init__(self, output_dir="views", entity_registry=None):
        self.output_dir = output_dir
        self.components = {}
        self.entity_registry = entity_registry if entity_registry is not None else {}

    def register_component(self, node: UIComponentNode):
        self.components[node.name] = node

    def generate_page(self, node: UIPageNode, output_dir: str = "views"):
        html_body = self._generate_elements(node.elements)
        
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{node.name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
    <div class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
{html_body}
    </div>
</body>
</html>"""
        
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{node.name}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        return file_path

    def _generate_elements(self, elements, indent_level=2):
        html_parts = []
        indent = "    " * indent_level
        
        for el in elements:
            html_parts.append(self._generate_element(el, indent_level))
            
        return "\n".join(html_parts)

    def _generate_element(self, el: UIElementNode, indent_level: int) -> str:
        indent = "    " * indent_level
        val_str = ""
        if isinstance(el.value, TextNode):
            val_str = el.value.value
        elif hasattr(el.value, 'name'):
            # Data Binding: VariableNode -> {{ variable }}
            val_str = f"{{{{ {el.value.name} }}}}"

        if el.element_type == "component_ref":
            comp_name = val_str
            if comp_name in self.components:
                # Wrap component in a section to namespace it
                comp_html = self._generate_elements(self.components[comp_name].elements, indent_level + 1)
                return f'{indent}<section class="component-{comp_name.lower()} mb-8">\n{comp_html}\n{indent}</section>'
            else:
                return f"{indent}<!-- Missing Component: {comp_name} -->"

        elif el.element_type == "heading":
            return f'{indent}<h1 class="text-4xl font-bold text-gray-900 mb-6">{val_str}</h1>'
            
        elif el.element_type == "text":
            return f'{indent}<p class="text-lg text-gray-700 mb-4 leading-relaxed">{val_str}</p>'
            
        elif el.element_type == "button":
            btn_text = val_str if val_str else "Click Me"
            return f'{indent}<button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg shadow-sm transition duration-150 ease-in-out">{btn_text}</button>'
            
        elif el.element_type == "navbar":
            return f'{indent}<nav class="bg-white shadow-sm border border-gray-200 rounded-xl px-6 py-4 mb-8 flex justify-between items-center"><div class="text-xl font-bold text-blue-600">Logo</div><div class="space-x-4"><a href="#" class="text-gray-600 hover:text-gray-900">Home</a><a href="#" class="text-gray-600 hover:text-gray-900">About</a></div></nav>'
            
        elif el.element_type == "image":
            alt = val_str if val_str else "Image"
            src = "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80"
            return f'{indent}<img src="{src}" alt="{alt}" class="rounded-xl shadow-md mb-6 w-full object-cover h-64" />'
            
        elif el.element_type == "input":
            placeholder = val_str if val_str else "Enter text..."
            # Simple form data binding support
            name_attr = f'name="{el.value.name}"' if hasattr(el.value, 'name') else ''
            return f'{indent}<input type="text" placeholder="{placeholder}" {name_attr} class="border border-gray-300 rounded-lg px-4 py-3 w-full mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition" />'

        elif el.element_type == "chart":
            title = val_str if val_str else "Analytics"
            return f'{indent}<div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-6"><h3 class="text-lg font-medium text-gray-900 mb-4">{title}</h3><div class="h-64 flex items-center justify-center text-gray-400 bg-gray-50 rounded border border-dashed border-gray-200">[ Chart Container ]</div></div>'
            
        elif el.element_type == "badge":
            return f'{indent}<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800">{val_str}</span>'
            
        elif el.element_type == "alert":
            return f'{indent}<div class="bg-amber-50 border-l-4 border-amber-400 p-4 mb-6"><div class="flex"><div class="ml-3"><p class="text-sm text-amber-800">{val_str}</p></div></div></div>'

        # Block elements
        children_html = ""
        if el.children:
            children_html = "\n" + self._generate_elements(el.children, indent_level + 1) + f"\n{indent}"
            
        if el.element_type == "card":
            return f'{indent}<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6 hover:shadow-md transition">{children_html}</div>'
            
        elif el.element_type == "row":
            return f'{indent}<div class="flex flex-row flex-wrap gap-6 mb-6">{children_html}</div>'
            
        elif el.element_type == "column":
            return f'{indent}<div class="flex flex-col gap-4 mb-6">{children_html}</div>'
            
        elif el.element_type == "form":
            # Smart Form Inference
            if hasattr(el.value, 'name') and el.value.name in self.entity_registry:
                entity_name = el.value.name
                fields = self.entity_registry[entity_name]
                auto_inputs = ""
                for field in fields:
                    if field['name'] == 'created_at': continue
                    label = field['name'].replace('_', ' ').title()
                    auto_inputs += f'\n{indent}    <div class="mb-4"><label class="block text-sm font-medium text-gray-700 mb-1">{label}</label><input type="text" name="{field["name"]}" class="border border-gray-300 rounded-lg px-4 py-2 w-full focus:ring-blue-500 focus:border-blue-500 transition" /></div>'
                auto_inputs += f'\n{indent}    <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg mt-4 transition">Save {entity_name}</button>'
                children_html = auto_inputs + children_html
                
            return f'{indent}<form class="bg-white rounded-xl shadow-sm border border-gray-100 p-8 mb-6">{children_html}</form>'
            
        elif el.element_type == "table":
            title = val_str if val_str else "Data"
            thead = ""
            
            # Smart Table Inference
            if hasattr(el.value, 'name') and el.value.name in self.entity_registry:
                entity_name = el.value.name
                title = f"{entity_name} Records"
                fields = self.entity_registry[entity_name]
                th_html = ""
                for field in fields:
                    label = field['name'].replace('_', ' ').title()
                    th_html += f'<th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{label}</th>'
                thead = f"<thead><tr>{th_html}<th class=\"px-6 py-3 bg-gray-50 text-right text-xs font-medium text-gray-500 uppercase tracking-wider\">Actions</th></tr></thead>"
                
                # Jinja body
                row_html = "{% for row in " + entity_name + " %}\n<tr>"
                for field in fields:
                    fname = field['name']
                    row_html += f'<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{{{ row.{fname} }}}}</td>'
                
                # Actions (Update and Delete using internal forms)
                actions = f'''
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <form method="POST" action="/{entity_name.lower()}s/update" class="inline">
                        <input type="hidden" name="_method" value="PUT">
                        <input type="hidden" name="id" value="{{{{ row.id }}}}">
                        <input type="text" name="{fields[0]['name']}" value="UPDATED_VALUE" class="hidden">
                        <button type="submit" class="text-blue-600 hover:text-blue-900 mr-2">Update</button>
                    </form>
                    <form method="POST" action="/{entity_name.lower()}s/delete" class="inline">
                        <input type="hidden" name="_method" value="DELETE">
                        <input type="hidden" name="id" value="{{{{ row.id }}}}">
                        <button type="submit" class="text-red-600 hover:text-red-900">Delete</button>
                    </form>
                </td>
                '''
                row_html += actions + "</tr>\n{% endfor %}"
                children_html = row_html
            
            return f'{indent}<div class="bg-white shadow-sm rounded-xl border border-gray-100 mb-6 overflow-hidden"><div class="px-6 py-4 border-b border-gray-200"><h3 class="text-lg font-medium text-gray-900">{title}</h3></div><div class="overflow-x-auto"><table class="min-w-full divide-y divide-gray-200">{thead}<tbody class="bg-white divide-y divide-gray-200">{children_html}</tbody></table></div></div>'
            
        elif el.element_type == "sidebar":
            return f'{indent}<aside class="w-64 bg-gray-900 text-white min-h-screen p-6 shadow-xl flex-shrink-0">{children_html}</aside>'
            
        elif el.element_type == "dashboard":
            # Dashboard is a full wrapper
            return f'{indent}<div class="flex h-screen bg-gray-50 overflow-hidden w-full">{children_html}</div>'
            
        elif el.element_type == "tabs":
            return f'{indent}<div class="border-b border-gray-200 mb-6"><nav class="-mb-px flex space-x-8">{children_html}</nav></div>'
            
        return f"{indent}<!-- Unknown UI Element: {el.element_type} -->"
