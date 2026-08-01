from lsprotocol.types import Location

class DefinitionProvider:
    def __init__(self, workspace):
        self.workspace = workspace

    def get_definition(self, uri, position):
        # Basic mock definition for v1
        return None
