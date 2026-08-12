class QueryNode: pass
class InsertNode(QueryNode):
    def __init__(self, model_name, fields):
        self.model_name = model_name
        self.fields = fields
class FindNode(QueryNode):
    def __init__(self, model_name):
        self.model_name = model_name
class UpdateNode(QueryNode):
    def __init__(self, model_name, fields):
        self.model_name = model_name
        self.fields = fields
class DeleteNode(QueryNode):
    def __init__(self, model_name):
        self.model_name = model_name
