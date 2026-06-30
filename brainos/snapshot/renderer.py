from .model import ProjectSnapshot

class SnapshotRenderer:
    def render(self, model: ProjectSnapshot, filepath: str):
        content = f"""# Project Snapshot

## Identity
──────────────
**Project** : {model.project_name}
**Version** : {model.version}

## Current State
──────────────
**Milestone** : {model.milestone}
**Phase** : {model.phase}

## Completed
──────────────
"""
        for c in model.completed:
            content += f"✓ {c}\n"
            
        content += "\n## Frozen\n──────────────\n"
        for f in model.frozen:
            content += f"✓ {f}\n"
            
        content += "\n## Architecture Freeze Matrix\n──────────────\n\n| Component        | Status            |\n| ---------------- | ----------------- |\n"
        for comp, status in model.matrix.items():
            content += f"| {comp:<16} | {status:<17} |\n"
            
        content += "\n## Technical Debt\n──────────────\n"
        for d in model.debt:
            content += f"• {d}\n"
            
        content += f"\n## Current Branch\n──────────────\n{model.branch}\n"
        content += f"\n## Next Target\n──────────────\n{model.next_target}\n"
        content += f"\n## Regression Risk\n──────────────\n{model.regression_risk}\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
