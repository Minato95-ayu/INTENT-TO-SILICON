class PackageError(Exception):
    pass

class ManifestError(PackageError):
    pass

class CircularDependencyError(PackageError):
    pass

class ResolutionError(PackageError):
    pass

class ChecksumMismatchError(PackageError):
    pass

class NetworkError(PackageError):
    pass

class PackageNotFoundError(PackageError):
    pass
