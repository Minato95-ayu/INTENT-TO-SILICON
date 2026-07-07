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
