import json
import threading
import time
import hashlib
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from runtime.ui.render_tree import RenderTree, RenderNode
from runtime.events.queue import EventQueue, ActionEvent

_session_manager = None
_global_project_dir = "."

def generate_css_class(props: dict) -> tuple[str, str]:
    import hashlib
    css_props = []
    responsive_props = {"mobile": [], "tablet": [], "desktop": []}
    
    mapping = {
        "width": "width", "height": "height", "backgroundColor": "background-color",
        "background": "background", "color": "color", "padding": "padding", 
        "margin": "margin", "borderRadius": "border-radius", "radius": "border-radius",
        "fontSize": "font-size", "fontWeight": "font-weight", 
        "justifyContent": "justify-content", "alignItems": "align-items", 
        "gap": "gap", "border": "border", "cursor": "cursor", 
        "overflowY": "overflow-y", "overflow": "overflow", "shadow": "box-shadow", 
        "gradient": "background", "flex": "flex", "flexGrow": "flex-grow",
        "display": "display", "flexDirection": "flex-direction",
        "minWidth": "min-width", "maxWidth": "max-width",
        "minHeight": "min-height", "maxHeight": "max-height"
    }
    
    def fmt_val(k, v):
        val = str(v)
        if (k in ["fontSize", "radius", "borderRadius", "padding", "margin", "width", "height"]) and val.isdigit(): 
            val += "px"
        if k == "gradient":
            val = f"linear-gradient({val})"
        return val
    
    for k, v in props.items():
        if k in mapping:
            css_props.append(f"{mapping[k]}: {fmt_val(k, v)};")
            
    if "__responsive__" in props:
        for k, breakpoints in props["__responsive__"].items():
            if k in mapping:
                if "mobile" in breakpoints:
                    responsive_props["mobile"].append(f"{mapping[k]}: {fmt_val(k, breakpoints['mobile'])};")
                if "tablet" in breakpoints:
                    responsive_props["tablet"].append(f"{mapping[k]}: {fmt_val(k, breakpoints['tablet'])};")
                if "desktop" in breakpoints:
                    responsive_props["desktop"].append(f"{mapping[k]}: {fmt_val(k, breakpoints['desktop'])};")
                    
    if not css_props and not responsive_props["mobile"] and not responsive_props["tablet"] and not responsive_props["desktop"] and "hoverBackgroundColor" not in props and "hoverColor" not in props:
        return "", ""
        
    # Serialize props for hashing to create a unique class name
    content = str(sorted([(k, str(v)) for k, v in props.items()]))
    class_name = "cls-" + hashlib.md5(content.encode()).hexdigest()[:8]
    
    css_rule = f".{class_name} {{ {' '.join(css_props)} }}\n"
    if responsive_props["mobile"]:
        css_rule += f"@media (max-width: 480px) {{ .{class_name} {{ {' '.join(responsive_props['mobile'])} }} }}\n"
    if responsive_props["tablet"]:
        css_rule += f"@media (min-width: 481px) and (max-width: 1024px) {{ .{class_name} {{ {' '.join(responsive_props['tablet'])} }} }}\n"
    if responsive_props["desktop"]:
        css_rule += f"@media (min-width: 1025px) {{ .{class_name} {{ {' '.join(responsive_props['desktop'])} }} }}\n"
        
    # Add hover state if hoverBackgroundColor exists
    if "hoverBackgroundColor" in props:
        css_rule += f".{class_name}:hover {{ background-color: {props['hoverBackgroundColor']} !important; }}\n"
    if "hoverColor" in props:
        css_rule += f".{class_name}:hover {{ color: {props['hoverColor']} !important; }}\n"
        
    return class_name, css_rule

def serialize_node(node: RenderNode, style_sheet: set):
    props = {}
    for k, v in node.props.items():
        if isinstance(v, str) and v.startswith("Theme."):
            props[k] = f"var(--{v.split('.')[1]})"
        else:
            props[k] = v
    node_type = node.type.lower()
    
    if node_type == "row":
        props["display"] = "flex"
        props["flexDirection"] = "row"
        if "gap" not in props: props["gap"] = "0px"
    elif node_type == "column":
        props["display"] = "flex"
        props["flexDirection"] = "column"
        if "gap" not in props: props["gap"] = "0px"
    elif node_type == "center":
        props["display"] = "flex"
        props["justifyContent"] = "center"
        props["alignItems"] = "center"
    elif node_type == "expanded":
        props["flex"] = "1"
    elif node_type == "spacer":
        props["flexGrow"] = "1"
    elif node_type == "padding":
        # Usually padding widget just applies padding prop
        if "value" in props:
            props["padding"] = props.pop("value")
    elif node_type == "scrollview":
        props["overflowY"] = "auto"
        props["display"] = "flex"
        props["flexDirection"] = "column"
    elif node_type == "page":
        props["display"] = "flex"
        props["flexDirection"] = "column"
        props["width"] = "100vw"
        props["height"] = "100vh"
        props["margin"] = "0"
        props["overflow"] = "hidden"
    elif node_type == "grid":
        cols = props.get("columns", 2)
        gap = props.get("gap", "10px")
        props["display"] = "grid"
        props.pop("columns", None)  # not a CSS property
    elif node_type in ("container", "card"):
        props["display"] = "flex"
        props["flexDirection"] = "column"
    elif node_type == "appbar":
        props["display"] = "flex"
        props["flexDirection"] = "row"
        props["alignItems"] = "center"
        if "height" not in props: props["height"] = "56px"
    elif node_type == "navigationbar":
        props["display"] = "flex"
        props["flexDirection"] = "row"
        props["alignItems"] = "center"
        if "height" not in props: props["height"] = "56px"
    elif node_type in ("list", "form"):
        props["display"] = "flex"
        props["flexDirection"] = "column"
    elif node_type == "stack":
        props["position"] = "relative"
    elif node_type == "divider":
        if "height" not in props: props["height"] = "1px"
        props["width"] = "100%"
    

    elif node_type == "scaffold":
        props["display"] = "flex"
        props["flexDirection"] = "column"
        props["width"] = "100vw"
        props["height"] = "100vh"
        props["margin"] = "0"
        props["overflow"] = "hidden"
    elif node_type == "avatar":
        props["display"] = "flex"
        props["alignItems"] = "center"
        props["justifyContent"] = "center"
        if "size" in props:
            sz = str(props["size"])
            if sz.isdigit(): sz += "px"
            props["width"] = sz
            props["height"] = sz
            props["borderRadius"] = "50%"
            props.pop("size")
    elif node_type == "chatbubble":
        props["display"] = "flex"
        props["flexDirection"] = "column"
        if props.get("sender") == "true":
            props["alignSelf"] = "flex-end"
            if "backgroundColor" not in props:
                props["backgroundColor"] = "#005c4b"
        else:
            props["alignSelf"] = "flex-start"
            if "backgroundColor" not in props:
                props["backgroundColor"] = "#202c33"
        props["borderRadius"] = "8px"
        props["padding"] = "6px 8px"
        props["margin"] = "4px 0"
        
    class_name, css_rule = generate_css_class(props)
    if css_rule:
        style_sheet.add(css_rule)
        
    return {
        "id": node.id,
        "type": node_type,
        "class": class_name,
        "props": props,
        "children": [serialize_node(c, style_sheet) for c in node.children]
    }

class WebRendererHandler(BaseHTTPRequestHandler):

    def get_session_id(self):
        import http.cookies
        cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        if 'session_id' in cookies:
            return cookies['session_id'].value
        return None

    def do_GET(self):
        session_id = self.get_session_id()
        session = _session_manager.get_or_create_session(session_id)
        
        # API Stream
        if self.path == "/api/stream":
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            if session_id != session.session_id:
                self.send_header('Set-Cookie', f'session_id={session.session_id}; Path=/')
            self.end_headers()
            
            try:
                initial = f"data: {session.current_tree_json}\n\n"
                self.wfile.write(initial.encode('utf-8'))
                self.wfile.flush()
                
                while True:
                    data = session.message_queue.get()
                    msg = f"data: {data}\n\n"
                    self.wfile.write(msg.encode('utf-8'))
                    self.wfile.flush()
            except Exception:
                pass
            return
            
        # Serve Static Assets from .aayu/build/
        import os
        import mimetypes
        
        req_path = self.path
        if req_path == "/":
            req_path = "/index.html"
            
        build_dir = os.path.join(_global_project_dir, ".aayu", "build")
        file_path = os.path.abspath(os.path.join(build_dir, req_path.lstrip("/")))
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type:
                self.send_header("Content-type", mime_type)
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            if session_id != session.session_id:
                self.send_header('Set-Cookie', f'session_id={session.session_id}; Path=/')
            self.end_headers()
            
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        session_id = self.get_session_id()
        session = _session_manager.get_session(session_id)
        if not session:
            self.send_response(401)
            self.end_headers()
            return
            
        if self.path == "/api/action":
            content_length = int(self.headers.get('Content-Length', 0))
            action_name = self.rfile.read(content_length).decode('utf-8')
            session.event_queue.push(ActionEvent(action_name))
            self.send_response(200)
            self.end_headers()
            
        elif self.path == "/api/event":
            import json
            from runtime.events.queue import InputEvent
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                evt_type = data.get("type")
                target = data.get("target")
                val = data.get("value")
                
                if evt_type == "INPUT":
                    session.event_queue.push(InputEvent(target, val))
                elif evt_type == "ACTION":
                    session.event_queue.push(ActionEvent(target))
                    
                self.send_response(200)
                self.end_headers()
            except Exception as e:
                print("Event processing error:", e)
                self.send_response(400)
                self.end_headers()
            
    def log_message(self, format, *args):
        pass


class WebRenderer:
    _instance = None

    @classmethod
    def instance(cls) -> "WebRenderer":
        if cls._instance is None:
            raise RuntimeError("WebRenderer not initialized.")
        return cls._instance

    def __init__(self, session_manager, project_dir: str = ".", port: int = 3000):
        WebRenderer._instance = self
        self.session_manager = session_manager
        self.port = port
        self.server = None
        self.thread = None
        
        global _session_manager, _global_project_dir
        _session_manager = session_manager
        _global_project_dir = project_dir

    def broadcast_theme_update(self, theme_name: str):
        from runtime.ui.theme import ThemeManager
        theme = ThemeManager.instance()._themes.get(theme_name, {})
        data = {
            "type": "theme",
            "cssVars": {f"--{k}": (f"{v}px" if isinstance(v, (int, float)) else v) for k, v in theme.items()}
        }
        import json
        msg = json.dumps(data)
        
        # Broadcast to all sessions
        if _session_manager:
            for session in _session_manager.sessions.values():
                try:
                    session.message_queue.put_nowait(msg)
                except:
                    pass



    def initialize(self):
        import os
        build_dir = os.path.join(_global_project_dir, ".aayu", "build")
        os.makedirs(build_dir, exist_ok=True)
        
        with open(os.path.join(build_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AAYU DOM Renderer</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/styles.css">
    <link rel="stylesheet" id="theme-css" href="/theme.css">
    <style id="dynamic-styles"></style>
</head>
<body>
    <div id="root"></div>
    <script src="/app.js"></script>
</body>
</html>''')
            
        with open(os.path.join(build_dir, "styles.css"), "w", encoding="utf-8") as f:
            f.write('''body { margin: 0; padding: 0; font-family: var(--font, 'Segoe UI'), Helvetica, Arial, sans-serif; background-color: var(--background, #111b21); color: var(--text, #e9edef); overflow: hidden; }
.widget-container { box-sizing: border-box; display: flex; }
.widget-row { display: flex; flex-direction: row; box-sizing: border-box; }
.widget-column { display: flex; flex-direction: column; box-sizing: border-box; }
.widget-button { cursor: pointer; border: none; outline: none; box-sizing: border-box; transition: background-color 0.2s; display: flex; align-items: center; justify-content: center;}
.widget-input { border: 1px solid #ccc; outline: none; box-sizing: border-box; padding: 0 15px; font-family: inherit; }
.widget-icon { display: flex; align-items: center; justify-content: center; }
.widget-page, .widget-scaffold { width: 100vw; height: 100vh; overflow: hidden; box-sizing: border-box; display: flex; flex-direction: column; background-color: var(--background, #111b21); }
.widget-text { font-family: inherit; color: var(--text, #e9edef); }
.widget-avatar { object-fit: cover; overflow: hidden; background-color: #ccc; }
.widget-chatbubble { max-width: 85%; font-size: 14.2px; }
.chat-time { font-size: 11px; color: rgba(255,255,255,0.6); align-self: flex-end; margin-top: 4px; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }

#root { width: 100vw; height: 100vh; }
''')
            
        with open(os.path.join(build_dir, "app.js"), "w", encoding="utf-8") as f:
            f.write('''const rootEl = document.getElementById('root');
const styleEl = document.getElementById('dynamic-styles');

const iconMap = {
    'search': 'fa-search', 'menu': 'fa-ellipsis-v', 'back': 'fa-arrow-left',
    'plus': 'fa-plus', 'send': 'fa-paper-plane', 'user': 'fa-user',
    'check': 'fa-check', 'check-double': 'fa-check-double'
};

function sendEvent(type, target, value) {
    fetch("/api/event", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, target, value })
    });
}

function createElementFromNode(node) {
    let el;
    const t = node.type;
    if (t === "text") {
        el = document.createElement("span");
        el.className = "widget-text";
        el.innerText = node.props.text || node.props.value || "";
    } else if (t === "heading") {
        el = document.createElement("h1");
        el.innerText = node.props.text || node.props.value || "";
        el.style.margin = "0";
    } else if (t === "button") {
        el = document.createElement("button");
        el.innerText = node.props.text || node.props.value || "";
        el.className = "widget-button";
    } else if (t === "input" || t === "passwordinput") {
        el = document.createElement("input");
        if (t === "passwordinput") el.type = "password";
        el.placeholder = node.props.placeholder || "";
        el.className = "widget-input";
        if (node.props.value) el.value = node.props.value;
        
        if (node.props.bind) {
            el.oninput = (e) => {
                sendEvent("INPUT", node.props.bind, e.target.value);
            };
        }
    } else if (t === "icon") {
        el = document.createElement("i");
        const iconName = node.props.name || "user";
        el.className = `widget-icon fas ${iconMap[iconName] || "fa-" + iconName}`;
    } else if (t === "image") {
        el = document.createElement("img");
        el.src = node.props.src || "";
        el.style.objectFit = "cover";
    } else if (t === "avatar") {
        if (node.props.src) {
            el = document.createElement("img");
            el.src = node.props.src;
        } else {
            el = document.createElement("div");
            el.innerText = node.props.text || "";
        }
        el.className = "widget-avatar widget-container";
    } else if (t === "divider") {
        el = document.createElement("div");
        el.style.height = "1px";
        el.style.width = "100%";
        el.style.backgroundColor = node.props.color || "#ccc";
    } else if (t === "row") {
        el = document.createElement("div");
        el.className = "widget-row";
    } else if (t === "column" || t === "list" || t === "scrollview") {
        el = document.createElement("div");
        el.className = "widget-column";
    } else if (t === "page" || t === "scaffold") {
        el = document.createElement("div");
        el.className = t === "page" ? "widget-page" : "widget-scaffold";
    } else if (t === "chatbubble") {
        el = document.createElement("div");
        el.className = "widget-chatbubble widget-container";
        // Text
        const tspan = document.createElement("span");
        tspan.innerText = node.props.text || node.props.value || "";
        el.appendChild(tspan);
        // Time & Ticks
        if (node.props.time) {
            const timeEl = document.createElement("div");
            timeEl.className = "chat-time";
            let content = node.props.time;
            if (node.props.seen === "true" || node.props.seen === true) {
                content += ' <i class="fas fa-check-double" style="color:#53bdeb; margin-left:4px;"></i>';
            }
            timeEl.innerHTML = content;
            el.appendChild(timeEl);
        }
    } else {
        el = document.createElement("div");
        el.className = "widget-container";
    }
    
    if (node.class) {
        el.classList.add(node.class);
    }
    
    if (node.props.onClick) {
        el.style.cursor = "pointer";
        el.onclick = (e) => {
            e.stopPropagation();
            sendEvent("ACTION", node.props.onClick, "");
        };
    }
    
    if (t !== "chatbubble" && node.children && node.children.length > 0) {
        node.children.forEach(child => {
            el.appendChild(createElementFromNode(child));
        });
    }
    
    el._vnode = node; 
    return el;
}

function patch(parent, oldEl, newVNode, index = 0) {
    if (!oldEl) {
        parent.appendChild(createElementFromNode(newVNode));
        return;
    }
    
    const oldVNode = oldEl._vnode;
    
    if (!oldVNode || oldVNode.type !== newVNode.type) {
        const newEl = createElementFromNode(newVNode);
        parent.replaceChild(newEl, oldEl);
        return;
    }
    
    if (oldVNode.class !== newVNode.class) {
        if (oldVNode.class) oldEl.classList.remove(oldVNode.class);
        if (newVNode.class) oldEl.classList.add(newVNode.class);
    }
    
    if (["text", "heading", "button"].includes(newVNode.type)) {
        const nt = newVNode.props.text || newVNode.props.value || "";
        const ot = oldVNode.props.text || oldVNode.props.value || "";
        if (nt !== ot) {
            oldEl.innerText = nt;
        }
    }
    
    if (newVNode.type === "input" || newVNode.type === "passwordinput") {
        if (oldEl.value !== newVNode.props.value && document.activeElement !== oldEl) {
            oldEl.value = newVNode.props.value || "";
        }
        if (oldVNode.props.placeholder !== newVNode.props.placeholder) {
            oldEl.placeholder = newVNode.props.placeholder || "";
        }
    }
    
    if (newVNode.type === "icon") {
        if (oldVNode.props.name !== newVNode.props.name) {
            const oldIcon = oldVNode.props.name || "user";
            const newIcon = newVNode.props.name || "user";
            oldEl.classList.remove(`fa-${oldIcon}`, iconMap[oldIcon] || `fa-${oldIcon}`);
            oldEl.classList.add(`fa-${newIcon}`, iconMap[newIcon] || `fa-${newIcon}`);
        }
    }
    
    if (newVNode.type === "chatbubble") {
        const oldT = oldVNode.props.text || oldVNode.props.value || "";
        const newT = newVNode.props.text || newVNode.props.value || "";
        if (oldT !== newT && oldEl.firstChild) {
            oldEl.firstChild.innerText = newT;
        }
    }
    
    if (newVNode.props.onClick !== oldVNode.props.onClick) {
        if (newVNode.props.onClick) {
            oldEl.style.cursor = "pointer";
            oldEl.onclick = (e) => {
                e.stopPropagation();
                sendEvent("ACTION", newVNode.props.onClick, "");
            };
        } else {
            oldEl.style.cursor = "";
            oldEl.onclick = null;
        }
    }
    
    oldEl._vnode = newVNode; 
    
    if (!["text", "heading", "button", "chatbubble"].includes(newVNode.type)) {
        const newChildren = newVNode.children || [];
        const oldChildNodes = Array.from(oldEl.childNodes);
        
        for (let i = 0; i < newChildren.length; i++) {
            patch(oldEl, oldChildNodes[i], newChildren[i], i);
        }
        
        for (let i = newChildren.length; i < oldChildNodes.length; i++) {
            oldEl.removeChild(oldChildNodes[i]);
        }
    }
}

function renderTree(data) {
    if (!data.tree) return;
    
    if (data.route && data.route.path) {
        if (window.location.pathname !== data.route.path) {
            window.history.pushState(null, "", data.route.path);
        }
    }
    
    const newStyles = data.styles.join('\\n');
    if (styleEl.innerHTML !== newStyles) {
        styleEl.innerHTML = newStyles;
    }
    
    const firstChild = rootEl.firstChild;
    if (!firstChild) {
        rootEl.appendChild(createElementFromNode(data.tree));
    } else {
        patch(rootEl, firstChild, data.tree);
    }
}

window.addEventListener('popstate', (event) => {
    sendEvent("ACTION", "sys_nav_back", "");
});

const evtSource = new EventSource('/api/stream');
evtSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'theme') {
        for (const key in data.cssVars) {
            document.documentElement.style.setProperty(key, data.cssVars[key]);
        }
        return;
    }
    renderTree(data);
};
''')
            
        from runtime.ui.theme import ThemeManager
        with open(os.path.join(build_dir, "theme.css"), "w", encoding="utf-8") as f:
            f.write(ThemeManager.instance().generate_css_variables())
            
        self.server = ThreadingHTTPServer(('0.0.0.0', self.port), WebRendererHandler)


        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print("\n=========================================")
        print("AAYU Web Renderer (DOM Mode) started!")
        print(f"Open in browser: http://localhost:{self.port}")
        print("=========================================\n")

    def render(self, tree: RenderTree):
        # We no longer process render tree here, each session handles it
        pass
        
    def process_events(self):
        # We no longer process events centrally
        pass
        time.sleep(0.016)
        
    def shutdown(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
