# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

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
