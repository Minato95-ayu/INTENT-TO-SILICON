"""AAYU Theme Engine

Provides a global theme system with custom themes defined in AAYU syntax.
Colors, typography, spacing, etc. are passed directly to CSS Variables on the client.
"""

from typing import Dict, Optional
import json

class ThemeManager:
    """Global singleton that manages registered themes and the active theme."""

    _instance: Optional["ThemeManager"] = None

    def __init__(self):
        # Maps theme name to its properties dictionary
        self._themes: Dict[str, Dict[str, str]] = {}
        self._active_theme: str = ""

    @classmethod
    def instance(cls) -> "ThemeManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def active_name(self) -> str:
        return self._active_theme
        
    @property
    def active_theme(self) -> Dict[str, str]:
        return self._themes.get(self._active_theme, {})

    def set_theme(self, name: str):
        """Switch the active theme."""
        if name in self._themes:
            self._active_theme = name
        else:
            print(f"Warning: Theme '{name}' not found. Available: {list(self._themes.keys())}")
            # Even if not found, we set it. It might be defined later.
            self._active_theme = name

    def register_theme(self, name: str, properties: Dict[str, str]):
        """Register a custom theme from AAYU source."""
        # Convert any python dict (string or dict object) to dict if necessary
        if isinstance(properties, str):
            try:
                # If properties was stringified by constant pool
                properties = eval(properties)
                if isinstance(properties, list):
                    # convert list of tuples to dict
                    properties = dict(properties)
            except Exception:
                properties = {}
        self._themes[name] = properties
        
        # If no active theme is set, use the first one registered
        if not self._active_theme:
            self._active_theme = name

    def generate_css_variables(self) -> str:
        """Generates the :root CSS block for the currently active theme."""
        if not self.active_theme:
            return ""
            
        css_lines = [":root {"]
        for key, value in self.active_theme.items():
            if isinstance(value, (int, float)):
                # If it's a number, assume px. (e.g. radius 12 -> 12px)
                # This could be more sophisticated, but simple is best for now
                value = f"{value}px"
            css_lines.append(f"  --{key}: {value};")
        css_lines.append("}")
        return "\n".join(css_lines)
