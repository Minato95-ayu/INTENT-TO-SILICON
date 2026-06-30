import re
from typing import Optional

class Version:
    def __init__(self, major: int, minor: int, patch: int, prerelease: Optional[str] = None, build: Optional[str] = None):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.build = build

    @classmethod
    def parse(cls, version_string: str) -> 'Version':
        # Simple semver parsing: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
        pattern = r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
        match = re.match(pattern, version_string.strip())
        
        if not match:
            raise ValueError(f"Invalid version string: '{version_string}'")
            
        return cls(
            major=int(match.group('major')),
            minor=int(match.group('minor')),
            patch=int(match.group('patch')),
            prerelease=match.group('prerelease'),
            build=match.group('build')
        )

    def __str__(self) -> str:
        ver = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            ver += f"-{self.prerelease}"
        if self.build:
            ver += f"+{self.build}"
        return ver

    def __repr__(self) -> str:
        return f"Version({self.__str__()})"
