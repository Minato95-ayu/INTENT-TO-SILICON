class StorageError(Exception): pass
class UniqueConstraintError(StorageError): pass
class ValidationError(StorageError): pass
