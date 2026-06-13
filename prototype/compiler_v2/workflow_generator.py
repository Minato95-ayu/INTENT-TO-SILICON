import yaml

class SemanticWorkflowGenerator:
    def generate(self, intent_graph_nodes):
        """
        Takes a topologically sorted list of intent nodes and generates
        a semantic YAML workflow.
        """
        if not intent_graph_nodes:
            return ""
            
        workflow = {"workflow": []}
        
        for node in intent_graph_nodes:
            step = {
                "domain": node["domain"],
                "issue": node["problem"]
            }
            workflow["workflow"].append(step)
            
        # Dump to YAML format
        # sort_keys=False preserves the topological order
        return yaml.dump(workflow, sort_keys=False, default_flow_style=False)
