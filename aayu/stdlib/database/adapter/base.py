class StorageAdapterBase:
    def execute_plan(self, plan):
        raise NotImplementedError
    def create_table(self, table_name, fields):
        raise NotImplementedError
