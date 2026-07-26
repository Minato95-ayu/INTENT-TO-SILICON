from typing import List, Dict, Any, Optional
from runtime.ui.render_tree import RenderNode
from runtime.ui.render_object import RenderObject


def parse_unit(val: Any, reference: float = 0.0, default: float = 0.0) -> float:
    """Parse a value with responsive units support.
    
    Supports: px, %, vw, vh, auto, plain numbers.
    reference = parent dimension used for % calculations.
    """
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return float(val)
    if not isinstance(val, str):
        return default
    val = val.strip()
    if val == "auto":
        return default  # auto resolved by context
    if val.endswith('%'):
        try:
            return reference * float(val[:-1]) / 100.0
        except ValueError:
            return default
    if val.endswith('vw'):
        try:
            return float(val[:-2])  # caller must multiply by viewport
        except ValueError:
            return default
    if val.endswith('vh'):
        try:
            return float(val[:-2])
        except ValueError:
            return default
    if val.endswith('px'):
        try:
            return float(val[:-2])
        except ValueError:
            return default
    try:
        return float(val)
    except ValueError:
        return default


# Backward compatible alias
def parse_px(val: Any, default: float = 0.0) -> float:
    return parse_unit(val, default=default)


class LayoutEngine:
    """Cross-platform layout engine.
    
    Computes absolute (x, y, width, height) for every RenderNode.
    Same logic runs for Web, Desktop, and Mobile renderers so
    layouts are pixel-identical across platforms.
    """

    def __init__(self, viewport_width: float, viewport_height: float):
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

    def calculate_layout(self, root: RenderNode) -> RenderObject:
        layout_root = self._build_layout_tree(root)
        self._measure(layout_root, self.viewport_width, self.viewport_height)
        self._resolve_flex(layout_root)
        self._layout(layout_root, 0, 0, self.viewport_width, self.viewport_height)
        return layout_root

    # ------------------------------------------------------------------
    # Tree construction
    # ------------------------------------------------------------------

    def _build_layout_tree(self, node: RenderNode) -> RenderObject:
        layout_node = RenderObject(node)
        for child in node.children:
            layout_node.add_child(self._build_layout_tree(child))
        return layout_node

    # ------------------------------------------------------------------
    # Measurement pass (intrinsic sizes)
    # ------------------------------------------------------------------

    def _get_style(self, node: RenderObject) -> dict:
        props = node.render_node.props
        return node.render_node.style if node.render_node.style else props

    def _measure(self, node: RenderObject, max_w: float, max_h: float):
        t = node.render_node.type.lower()
        style = self._get_style(node)
        padding = parse_unit(style.get("padding", 0), max_w)

        # Measure children first (bottom-up)
        for child in node.children:
            self._measure(child, max_w, max_h)

        # --- Leaf widgets ---
        if t == "text":
            text = node.render_node.props.get("text", node.render_node.props.get("value", ""))
            node.width = len(str(text)) * 8 + padding * 2
            node.height = 20 + padding * 2

        elif t == "heading":
            text = node.render_node.props.get("text", node.render_node.props.get("value", ""))
            node.width = len(str(text)) * 14 + padding * 2
            node.height = 30 + padding * 2

        elif t == "button":
            text = node.render_node.props.get("text", node.render_node.props.get("value", "Button"))
            node.width = len(str(text)) * 8 + 40 + padding * 2
            node.height = 30 + padding * 2

        elif t in ("input", "passwordinput"):
            node.width = parse_unit(style.get("width", 200), max_w)
            node.height = parse_unit(style.get("height", 36), max_h)

        elif t == "icon":
            node.width = parse_unit(style.get("width", 24), max_w)
            node.height = parse_unit(style.get("height", 24), max_h)

        elif t == "image":
            node.width = parse_unit(style.get("width", 100), max_w)
            node.height = parse_unit(style.get("height", 100), max_h)

        elif t == "avatar":
            sz = parse_unit(style.get("size", 40), max_w)
            node.width = sz
            node.height = sz

        elif t == "divider":
            node.width = max_w - padding * 2
            node.height = 1

        elif t == "spacer":
            # Spacer claims no intrinsic size; resolved during flex pass
            node.width = 0
            node.height = 0

        elif t == "progress":
            node.width = parse_unit(style.get("width", max_w - padding * 2), max_w)
            node.height = parse_unit(style.get("height", 4), max_h)

        elif t in ("checkbox", "radio", "switch"):
            node.width = parse_unit(style.get("width", 24), max_w)
            node.height = parse_unit(style.get("height", 24), max_h)

        elif t == "dropdown":
            node.width = parse_unit(style.get("width", 200), max_w)
            node.height = parse_unit(style.get("height", 36), max_h)

        # --- Container / Block widgets ---
        elif t in ("column", "page", "scrollview", "form", "list"):
            w = parse_unit(style.get("width", max_w), max_w)
            node.width = w if w > 0 else max_w
            spacing = parse_unit(style.get("gap", 0), max_h)
            total_h = padding * 2
            for i, c in enumerate(node.children):
                total_h += c.height
                if i > 0:
                    total_h += spacing
            node.height = parse_unit(style.get("height", total_h), max_h)

        elif t == "row":
            spacing = parse_unit(style.get("gap", 0), max_w)
            content_w = padding * 2
            for i, c in enumerate(node.children):
                content_w += c.width
                if i > 0:
                    content_w += spacing
            w = parse_unit(style.get("width", 0), max_w)
            node.width = w if w > 0 else content_w
            h = parse_unit(style.get("height", 0), max_h)
            content_h = max((c.height for c in node.children), default=30) + padding * 2
            node.height = h if h > 0 else content_h

        elif t in ("container", "card"):
            w = parse_unit(style.get("width", 0), max_w)
            h = parse_unit(style.get("height", 0), max_h)
            content_w = max((c.width for c in node.children), default=100) + padding * 2
            content_h = sum(c.height for c in node.children) + padding * 2
            node.width = w if w > 0 else content_w
            node.height = h if h > 0 else content_h

        elif t == "stack":
            node.width = max((c.width for c in node.children), default=100) + padding * 2
            node.height = max((c.height for c in node.children), default=100) + padding * 2

        elif t == "center":
            # Center wraps its children; takes parent dimensions
            node.width = parse_unit(style.get("width", max_w), max_w)
            node.height = parse_unit(style.get("height", max_h), max_h)

        elif t == "expanded":
            # Expanded fills remaining space; intrinsic = child size (resolved in flex pass)
            if node.children:
                node.width = max(c.width for c in node.children)
                node.height = max(c.height for c in node.children)
            else:
                node.width = 0
                node.height = 0

        elif t == "padding":
            pad = parse_unit(style.get("value", style.get("padding", 16)), max_w)
            if node.children:
                node.width = max(c.width for c in node.children) + pad * 2
                node.height = sum(c.height for c in node.children) + pad * 2
            else:
                node.width = pad * 2
                node.height = pad * 2

        elif t == "appbar":
            node.width = max_w
            node.height = parse_unit(style.get("height", 56), max_h)

        elif t == "navigationbar":
            node.width = max_w
            node.height = parse_unit(style.get("height", 56), max_h)

        elif t == "tabbar":
            node.width = max_w
            node.height = parse_unit(style.get("height", 48), max_h)

        elif t == "grid":
            cols = int(style.get("columns", 2))
            gap = parse_unit(style.get("gap", 10), max_w)
            col_w = (max_w - padding * 2 - gap * (cols - 1)) / cols
            rows_count = (len(node.children) + cols - 1) // cols
            row_h = max((c.height for c in node.children), default=50)
            node.width = max_w
            node.height = rows_count * row_h + (rows_count - 1) * gap + padding * 2

        elif t in ("dialog", "drawer", "snackbar"):
            w = parse_unit(style.get("width", 300), max_w)
            h = parse_unit(style.get("height", 200), max_h)
            content_h = sum(c.height for c in node.children) + padding * 2
            node.width = w
            node.height = h if h > content_h else content_h

        else:
            # Fallback: intrinsic from children
            node.width = parse_unit(style.get("width", max((c.width for c in node.children), default=100)), max_w)
            node.height = parse_unit(style.get("height", sum(c.height for c in node.children)), max_h)

    # ------------------------------------------------------------------
    # Flex resolution pass (Expanded / Spacer)
    # ------------------------------------------------------------------

    def _resolve_flex(self, node: RenderObject):
        """Distribute remaining space among Expanded and Spacer children."""
        t = node.render_node.type.lower()
        style = self._get_style(node)
        padding = parse_unit(style.get("padding", 0))
        spacing = parse_unit(style.get("gap", 0))

        flex_children = []
        fixed_total = 0.0

        is_row = (t == "row")
        is_col = t in ("column", "page", "scrollview", "form", "list")

        if is_row or is_col:
            for i, child in enumerate(node.children):
                ct = child.render_node.type.lower()
                if ct in ("expanded", "spacer"):
                    flex_children.append(child)
                else:
                    if is_row:
                        fixed_total += child.width
                    else:
                        fixed_total += child.height
                if i > 0:
                    if is_row:
                        fixed_total += spacing
                    else:
                        fixed_total += spacing

            if flex_children:
                available = (node.width if is_row else node.height) - padding * 2 - fixed_total
                if available < 0:
                    available = 0
                share = available / len(flex_children)
                for fc in flex_children:
                    if is_row:
                        fc.width = share
                        fc.height = node.height - padding * 2
                    else:
                        fc.height = share
                        fc.width = node.width - padding * 2

        # Recurse into all children
        for child in node.children:
            self._resolve_flex(child)

    # ------------------------------------------------------------------
    # Position pass (absolute x, y)
    # ------------------------------------------------------------------

    def _layout(self, node: RenderObject, x: float, y: float, w: float, h: float):
        node.x = x
        node.y = y

        t = node.render_node.type.lower()
        style = self._get_style(node)
        padding = parse_unit(style.get("padding", 0))
        spacing = parse_unit(style.get("gap", 0))

        justify = style.get("justifyContent", "flex-start")
        align = style.get("alignItems", "flex-start")

        current_x = x + padding
        current_y = y + padding

        if t in ("column", "page", "scrollview", "form", "list"):
            if justify == "center":
                total_h = sum(c.height for c in node.children) + spacing * max(len(node.children) - 1, 0)
                current_y = y + (node.height - total_h) / 2
            elif justify == "flex-end":
                total_h = sum(c.height for c in node.children) + spacing * max(len(node.children) - 1, 0)
                current_y = y + node.height - total_h - padding

            for child in node.children:
                child_x = current_x
                if align == "center":
                    child_x = x + (node.width - child.width) / 2
                elif align == "flex-end":
                    child_x = x + node.width - child.width - padding
                self._layout(child, child_x, current_y, child.width, child.height)
                current_y += child.height + spacing

        elif t == "row":
            if justify == "space-between" and len(node.children) > 1:
                total_w = sum(c.width for c in node.children)
                spacing = (node.width - padding * 2 - total_w) / (len(node.children) - 1)
            elif justify == "space-around" and len(node.children) > 0:
                total_w = sum(c.width for c in node.children)
                spacing = (node.width - padding * 2 - total_w) / (len(node.children) * 2)
                current_x += spacing
            elif justify == "center":
                total_w = sum(c.width for c in node.children) + spacing * max(len(node.children) - 1, 0)
                current_x = x + (node.width - total_w) / 2
            elif justify == "flex-end":
                total_w = sum(c.width for c in node.children) + spacing * max(len(node.children) - 1, 0)
                current_x = x + node.width - total_w - padding

            for child in node.children:
                child_y = current_y
                if align == "center":
                    child_y = y + (node.height - child.height) / 2
                elif align == "flex-end":
                    child_y = y + node.height - child.height - padding
                self._layout(child, current_x, child_y, child.width, child.height)
                current_x += child.width + spacing

        elif t in ("container", "card"):
            for child in node.children:
                child_x = current_x
                child_y = current_y
                if align == "center":
                    child_x = x + (node.width - child.width) / 2
                if justify == "center":
                    child_y = y + (node.height - child.height) / 2
                self._layout(child, child_x, child_y, child.width, child.height)
                current_y += child.height + spacing

        elif t == "center":
            for child in node.children:
                child_x = x + (node.width - child.width) / 2
                child_y = y + (node.height - child.height) / 2
                self._layout(child, child_x, child_y, child.width, child.height)

        elif t == "stack":
            for child in node.children:
                child_x = current_x
                child_y = current_y
                if align == "center":
                    child_x = x + (node.width - child.width) / 2
                if justify == "center":
                    child_y = y + (node.height - child.height) / 2
                self._layout(child, child_x, child_y, child.width, child.height)

        elif t == "grid":
            cols = int(style.get("columns", 2))
            gap = parse_unit(style.get("gap", 10))
            col_w = (node.width - padding * 2 - gap * (cols - 1)) / cols
            row_h = max((c.height for c in node.children), default=50)
            for i, child in enumerate(node.children):
                col_idx = i % cols
                row_idx = i // cols
                cx = current_x + col_idx * (col_w + gap)
                cy = current_y + row_idx * (row_h + gap)
                child.width = col_w
                self._layout(child, cx, cy, col_w, child.height)

        elif t in ("expanded", "padding"):
            for child in node.children:
                self._layout(child, current_x, current_y, child.width, child.height)

        elif t in ("appbar", "navigationbar", "tabbar"):
            # Lay children in a row inside the bar
            child_spacing = parse_unit(style.get("gap", 10))
            cx = current_x
            for child in node.children:
                child_y = y + (node.height - child.height) / 2  # vertical center
                self._layout(child, cx, child_y, child.width, child.height)
                cx += child.width + child_spacing

        else:
            for child in node.children:
                self._layout(child, current_x, current_y, child.width, child.height)
