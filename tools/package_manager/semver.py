import re

class SemVer:
    """Basic Semantic Versioning parser and matcher."""
    def __init__(self, version_str):
        self.raw = version_str
        self.operator = "="
        self.major = 0
        self.minor = 0
        self.patch = 0
        
        self._parse(version_str)
        
    def _parse(self, v):
        match = re.match(r'(^|\^|~|>=|<=|>|<|=)?(\d+)\.(\d+)\.(\d+)$', v.strip())
        if not match:
            # Fallback for simple versions or malformed
            return
        
        op = match.group(1)
        if op:
            self.operator = op
        self.major = int(match.group(2))
        self.minor = int(match.group(3))
        self.patch = int(match.group(4))
        
    def satisfies(self, available_version_str):
        avail = SemVer(available_version_str)
        
        if self.operator == "^":
            # Compatible with major
            return avail.major == self.major and (avail.minor > self.minor or (avail.minor == self.minor and avail.patch >= self.patch))
        elif self.operator == "~":
            # Compatible with minor
            return avail.major == self.major and avail.minor == self.minor and avail.patch >= self.patch
        elif self.operator == ">=":
            return (avail.major, avail.minor, avail.patch) >= (self.major, self.minor, self.patch)
        elif self.operator == "<=":
            return (avail.major, avail.minor, avail.patch) <= (self.major, self.minor, self.patch)
        elif self.operator == ">":
            return (avail.major, avail.minor, avail.patch) > (self.major, self.minor, self.patch)
        elif self.operator == "<":
            return (avail.major, avail.minor, avail.patch) < (self.major, self.minor, self.patch)
        else: # Exact match
            return avail.major == self.major and avail.minor == self.minor and avail.patch == self.patch
            
    def __str__(self):
        return self.raw
