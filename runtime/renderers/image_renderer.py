import os
from PIL import Image, ImageDraw, ImageFont
from runtime.ui.display_list import (
    DisplayList, DrawRect, DrawRoundedRect, DrawText, DrawLine, DrawImage, DrawIcon
)
class ImageRenderer:
    """
    A Headless Renderer that draws the DisplayList into a PNG image using Pillow.
    Useful for generating screenshots or running tests in CI without a display.
    """
    def __init__(self, width: int = 800, height: int = 600, output_path: str = "output.png"):
        self.width = width
        self.height = height
        self.output_path = output_path
        self.image = None
        self.draw = None

    def initialize(self):
        # Create a blank white image
        self.image = Image.new('RGB', (self.width, self.height), color='#ffffff')
        self.draw = ImageDraw.Draw(self.image)

    def render(self, display_list: DisplayList):
        # Re-initialize to clear previous frame if needed
        self.image = Image.new('RGB', (self.width, self.height), color='#ffffff')
        self.draw = ImageDraw.Draw(self.image)
        
        for command in display_list.commands:
            if isinstance(command, DrawRect):
                self.draw.rectangle(
                    [command.x, command.y, command.x + command.width, command.y + command.height],
                    fill=command.color
                )
            elif isinstance(command, DrawRoundedRect):
                # Pillow's rounded_rectangle
                self.draw.rounded_rectangle(
                    [command.x, command.y, command.x + command.width, command.y + command.height],
                    radius=command.radius,
                    fill=command.color
                )
            elif isinstance(command, DrawText):
                try:
                    # Try to load a generic truetype font if possible, else default
                    font = ImageFont.truetype("arial.ttf", command.font_size)
                except IOError:
                    font = ImageFont.load_default()
                    
                self.draw.text((command.x, command.y), command.text, fill=command.color, font=font)
                
            elif isinstance(command, DrawLine):
                self.draw.line(
                    [command.x1, command.y1, command.x2, command.y2],
                    fill=command.color,
                    width=command.thickness
                )
                
        # Save the image
        self.image.save(self.output_path)
        print(f"Image successfully rendered to {self.output_path}")

    def shutdown(self):
        pass
