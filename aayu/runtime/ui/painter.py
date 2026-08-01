from aayu.runtime.ui.render_object import RenderObject
from aayu.runtime.ui.display_list import (
    DisplayList, DrawRect, DrawRoundedRect, DrawText, RegisterClickArea,
    DrawLine, DrawCircle, DrawImage, DrawIcon
)

class Painter:
    """
    Paint Phase: Traverses RenderObjects and generates a DisplayList.
    """
    def paint(self, root: RenderObject) -> DisplayList:
        dl = DisplayList()
        if root:
            self._traverse(root, dl)
        return dl

    def _traverse(self, node: RenderObject, dl: DisplayList):
        t = node.render_node.type.lower()
        props = node.render_node.props
        style = node.render_node.style if node.render_node.style else props
        x, y, w, h = node.x, node.y, node.width, node.height
        
        bg_color = style.get('backgroundColor')
        
        def parse_px(val) -> float:
            if isinstance(val, str):
                return float(val.replace('px', '').replace('em', '').strip())
            return float(val) if val is not None else 0.0
            
        if t in ['container', 'card', 'page', 'row', 'column', 'stack']:
            if not bg_color:
                bg_color = '#ffffff' if t == 'page' else None
                
            if bg_color:
                radius = parse_px(style.get('borderRadius', 8.0 if t == 'card' else 0.0))
                if radius > 0:
                    dl.add(DrawRoundedRect(x, y, w, h, radius, bg_color))
                else:
                    dl.add(DrawRect(x, y, w, h, bg_color))
        
        elif t == 'button':
            bg_color = style.get('backgroundColor', '#0b9385') # WhatsApp green default
            text_color = style.get('color', '#ffffff')
            text = str(node.render_node.props.get('text', node.render_node.props.get('value', 'Button')))
            radius = parse_px(style.get('borderRadius', 20.0))
            
            dl.add(DrawRoundedRect(x, y, w, h, radius, bg_color))
            # Rough center text
            text_x = x + (w - len(text)*8)/2
            dl.add(DrawText(text_x, y + h/2 + 5, text, 'Helvetica', 14, text_color, bold=True))
            
            action = node.render_node.props.get('onClick')
            if action:
                dl.add(RegisterClickArea(x, y, w, h, action))
                
        elif t == 'text':
            text_color = style.get('color', '#000000')
            text = str(node.render_node.props.get('text', node.render_node.props.get('value', '')))
            font_size = int(style.get('fontSize', 14))
            bold = style.get('fontWeight') == 'bold'
            dl.add(DrawText(x, y + font_size + 2, text, 'Helvetica', font_size, text_color, bold=bold))
            
        elif t == 'heading':
            text_color = style.get('color', '#000000')
            text = str(node.render_node.props.get('text', node.render_node.props.get('value', '')))
            font_size = int(style.get('fontSize', 24))
            dl.add(DrawText(x, y + font_size + 4, text, 'Helvetica', font_size, text_color, bold=True))
            
        elif t == 'input':
            bg_color = style.get('backgroundColor', '#2a2f32') # WhatsApp dark input default
            text_color = style.get('color', '#ffffff')
            radius = parse_px(style.get('borderRadius', 20.0))
            placeholder = str(node.render_node.props.get('placeholder', ''))
            dl.add(DrawRoundedRect(x, y, w, h, radius, bg_color))
            dl.add(DrawText(x + 15, y + h/2 + 5, placeholder, 'Helvetica', 14, '#828689'))
            
        elif t == 'icon':
            # Simulated icon using DrawText emoji for now
            icon_name = str(node.render_node.props.get('name', '🔍'))
            color = style.get('color', '#828689')
            dl.add(DrawText(x, y + h/2 + 5, icon_name, 'Helvetica', 16, color))
            
        for child in node.children:
            self._traverse(child, dl)
