from typing import Dict, Any, List, Optional

class StorageAPI:
    def setup(self):
        raise NotImplementedError

    def add_node(self, node_id: str, node_type: str, name: str, data: Dict[str, Any]) -> None:
        raise NotImplementedError

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError
        
    def get_node_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    def get_nodes_by_type(self, node_type: str) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def add_edge(self, edge_id: str, from_node: str, to_node: str, relation: str, weight: float) -> None:
        raise NotImplementedError

    def get_edges(self, from_node: Optional[str] = None, to_node: Optional[str] = None, relation: Optional[str] = None) -> List[Dict[str, Any]]:
        raise NotImplementedError
