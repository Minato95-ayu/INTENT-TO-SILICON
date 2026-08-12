from typing import Any, Dict, List, Optional
from dataclasses import dataclass

class DrawingCommand:
    pass

@dataclass
class Save(DrawingCommand):
    pass

@dataclass
class Restore(DrawingCommand):
    pass

@dataclass
class Translate(DrawingCommand):
    dx: float
    dy: float

@dataclass
class ClipRect(DrawingCommand):
    x: float
    y: float
    width: float
    height: float

@dataclass
class DrawRect(DrawingCommand):
    x: float
    y: float
    width: float
    height: float
    color: str

@dataclass
class DrawRoundedRect(DrawingCommand):
    x: float
    y: float
    width: float
    height: float
    radius: float
    color: str

@dataclass
class DrawCircle(DrawingCommand):
    cx: float
    cy: float
    radius: float
    color: str

@dataclass
class DrawLine(DrawingCommand):
    x1: float
    y1: float
    x2: float
    y2: float
    color: str
    thickness: float = 1.0

@dataclass
class DrawImage(DrawingCommand):
    x: float
    y: float
    width: float
    height: float
    image_data: Any # Platform specific image handle or path

@dataclass
class DrawIcon(DrawingCommand):
    x: float
    y: float
    size: float
    icon_name: str
    color: str

@dataclass
class DrawText(DrawingCommand):
    x: float
    y: float
    text: str
    font_family: str
    font_size: int
    color: str
    bold: bool = False
    italic: bool = False

@dataclass
class RegisterClickArea(DrawingCommand):
    x: float
    y: float
    width: float
    height: float
    action_name: str
    cursor: str = "hand2" # Optional cursor hint

class DisplayList:
    def __init__(self):
        self.commands: List[DrawingCommand] = []
        
    def add(self, cmd: DrawingCommand):
        self.commands.append(cmd)

