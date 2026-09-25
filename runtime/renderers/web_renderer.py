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

import os
import json
import asyncio
from typing import Dict, Any
import mimetypes

from runtime.ui.render_tree import RenderTree, RenderNode

_global_project_dir = "."

iconMap = {
    "user": "fa-user",
    "search": "fa-search",
    "home": "fa-home",
    "settings": "fa-cog",
    "cart": "fa-shopping-cart",
    "heart": "fa-heart",
    "star": "fa-star",
    "bell": "fa-bell"
}

def serialize_node(node, style_sheet: set):
    node_type = node.widget_type.lower()
    
    props = {}
    for k, v in node.props.items():
        props[k] = v.to_python() if hasattr(v, 'to_python') else v
        
    class_name = None
    style_rules = []
    
    mapping = {
        'padding': 'padding', 'margin': 'margin', 'color': 'color',
        'backgroundColor': 'background-color', 'width': 'width',
        'height': 'height', 'size': 'font-size', 'border': 'border',
        'borderRadius': 'border-radius', 'shadow': 'box-shadow',
        'opacity': 'opacity', 'align': 'text-align',
        'position': 'position', 'zIndex': 'z-index', 'top': 'top',
        'left': 'left', 'marginTop': 'margin-top', 'marginBottom': 'margin-bottom',
        'paddingTop': 'padding-top', 'paddingBottom': 'padding-bottom', 'right': 'right', 'bottom': 'bottom'
    }
    
    def fmt_val(prop, v):
        if prop in ['padding', 'margin', 'width', 'height', 'size', 'border-radius', 'top', 'left', 'bottom', 'right', 'margin-top', 'margin-bottom', 'padding-top', 'padding-bottom']:
            if isinstance(v, (int, float)):
                return f"{v}px"
            if str(v).isdigit():
                return f"{v}px"
        return str(v)

    for p, v in props.items():
        if p in mapping:
            style_rules.append(f"{mapping[p]}: {fmt_val(mapping[p], v)}")
            
    if style_rules:
        class_name = f"aayu-{node.id}"
        rule = f".{class_name} {{ {'; '.join(style_rules)} }}"
        style_sheet.add(rule)
        
    return {
        "id": node.id,
        "type": node_type,
        "class": class_name,
        "props": props,
        "children": [serialize_node(c, style_sheet) for c in node.children]
    }

class WebRenderer:
    def __init__(self, session_manager, project_dir: str = ".", port: int = 4000):
        global _global_project_dir
        _global_project_dir = project_dir
        self.session_manager = session_manager
        self.project_dir = project_dir
        self.port = port
        self.build_dir = os.path.join(self.project_dir, ".aayu", "build")
        os.makedirs(self.build_dir, exist_ok=True)
        self.server = None
        self.thread = None
        
    async def asgi_app(self, scope, receive, send):
        if scope['type'] != 'http':
            return
            
        path = scope['path']
        if path == "/": path = "/index.html"
        
        headers = dict(scope.get('headers', []))
        cookie_header = headers.get(b'cookie', b'').decode('utf-8')
        session_id = None
        for cookie in cookie_header.split(';'):
            if 'session_id=' in cookie:
                session_id = cookie.split('session_id=')[1].strip()
                
        session = self.session_manager.get_or_create_session(session_id)
        
        if path == "/api/stream":
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', b'text/event-stream'],
                    [b'cache-control', b'no-cache'],
                    [b'connection', b'keep-alive'],
                ] + ([[b'set-cookie', f'session_id={session.session_id}; Path=/'.encode()]] if session_id != session.session_id else [])
            })
            
            try:
                initial = f"data: {session.current_tree_json}\n\n"
                await send({'type': 'http.response.body', 'body': initial.encode('utf-8'), 'more_body': True})
                
                while True:
                    try:
                        data = await asyncio.wait_for(session.message_queue.get(), timeout=15)
                        msg = f"data: {data}\n\n"
                        await send({'type': 'http.response.body', 'body': msg.encode('utf-8'), 'more_body': True})
                    except asyncio.TimeoutError:
                        await send({'type': 'http.response.body', 'body': b': keepalive\n\n', 'more_body': True})
            except asyncio.CancelledError:
                pass
            return
            
        if path == "/api/event":
            body = b''
            more_body = True
            while more_body:
                message = await receive()
                body += message.get('body', b'')
                more_body = message.get('more_body', False)
                
            data = json.loads(body)
            evt_type = data.get("type")
            target = data.get("target")
            val = data.get("value")
            
            from runtime.events.queue import ActionEvent, InputEvent
            if evt_type == "ACTION":
                session.event_queue.push(ActionEvent(target))
            elif evt_type == "INPUT":
                session.event_queue.push(InputEvent(target, val))
                
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [[b'content-type', b'application/json']]
            })
            await send({'type': 'http.response.body', 'body': b'{"status": "ok"}'})
            return
            
        file_path = os.path.abspath(os.path.join(self.build_dir, path.lstrip("/")))
        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [[b'content-type', (mime_type or 'application/octet-stream').encode()]]
            })
            with open(file_path, 'rb') as f:
                await send({'type': 'http.response.body', 'body': f.read()})
            return
            
        await send({'type': 'http.response.start', 'status': 404})
        await send({'type': 'http.response.body', 'body': b'Not Found'})

    def initialize(self):
        pass

    def start(self):
        with open(os.path.join(self.build_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AAYU Web App</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/theme.css">
    <style id="aayu-styles"></style>
    <style>
        body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        .widget-container { display: flex; flex-direction: column; }
        .row { flex-direction: row; }
        .center { align-items: center; justify-content: center; display: flex; width: 100%; height: 100%; }
        .expanded { flex: 1; }
        .padding { padding: 16px; }
        .card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow: hidden; }
        .button { background: #2196F3; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; text-align: center; }
        .button:hover { background: #1976D2; }
        .input { border: 1px solid #ccc; padding: 8px; border-radius: 4px; outline: none; }
        .input:focus { border-color: #2196F3; }
        .chatbubble { background: #E3F2FD; padding: 12px; border-radius: 12px; max-width: 70%; margin: 4px 0; word-wrap: break-word; position: relative; }
        .chat-time { font-size: 0.7em; color: #666; text-align: right; margin-top: 4px; }
    </style>
</head>
<body>
    <div id="root"></div>
    <script src="/app.js?v=2"></script>
</body>
</html>''')

        with open(os.path.join(self.build_dir, "app.js"), "w", encoding="utf-8") as f:
            f.write('''const rootEl = document.getElementById('root');
const styleEl = document.getElementById('aayu-styles');

const iconMap = {
    "user": "fa-user", "search": "fa-search", "home": "fa-home",
    "settings": "fa-cog", "cart": "fa-shopping-cart", "heart": "fa-heart",
    "star": "fa-star", "bell": "fa-bell"
};

function sendEvent(type, target, value) {
    fetch('/api/event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, target, value })
    });
}

function createElementFromNode(node) {
    if (!node) return document.createTextNode("");
    
    let el;
    const t = node.type;
    
    if (t === "text") {
        el = document.createElement("span");
        el.innerText = node.props.text || node.props.value || node.props.value_node || "";
    } else if (t === "heading") {
        el = document.createElement("h2");
        el.innerText = node.props.text || node.props.value || node.props.value_node || "";
    } else if (t === "button") {
        el = document.createElement("button");
        el.className = "button";
        el.innerText = node.props.text || node.props.value || node.props.value_node || "";
    } else if (t === "input" || t === "passwordinput") {
        el = document.createElement("input");
        el.className = "input";
        el.type = t === "passwordinput" ? "password" : "text";
        el.value = node.props.value || "";
        if (node.props.placeholder) el.placeholder = node.props.placeholder;
        
        let timeout = null;
        el.oninput = (e) => {
            if (node.props.bind) {
                clearTimeout(timeout);
                timeout = setTimeout(() => sendEvent("INPUT", node.props.bind, e.target.value), 50);
            }
        };
    } else if (t === "icon") {
        el = document.createElement("i");
        const iconName = node.props.name || "user";
        el.className = as ;
    } else if (t === "image") {
        el = document.createElement("img");
        if (node.props.src) el.src = node.props.src;
        if (node.props.width) el.width = parseInt(node.props.width);
        if (node.props.height) el.height = parseInt(node.props.height);
        el.style.objectFit = "cover";
    } else if (t === "chatbubble") {
        el = document.createElement("div");
        el.className = "chatbubble";
        
        const tspan = document.createElement("span");
        tspan.innerText = node.props.text || node.props.value || node.props.value_node || "";
        el.appendChild(tspan);
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
    
    if (node.props) {
        for (const key in node.props) {
            if (key.startsWith("aria-")) el.setAttribute(key, node.props[key]);
            else if (key === "role") el.setAttribute("role", node.props[key]);
            else if (key === "tabIndex") el.tabIndex = node.props[key];
            else if (key === "alt") el.alt = node.props[key];
        }
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
        const nt = newVNode.props.text || newVNode.props.value || newVNode.props.value_node || "";
        const ot = oldVNode.props.text || oldVNode.props.value || oldVNode.props.value_node || "";
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
            oldEl.classList.remove(a-, iconMap[oldIcon] || a-);
            oldEl.classList.add(a-, iconMap[newIcon] || a-);
        }
    }
    
    if (newVNode.type === "chatbubble") {
        const oldT = oldVNode.props.text || oldVNode.props.value || oldVNode.props.value_node || "";
        const newT = newVNode.props.text || newVNode.props.value || oldVNode.props.value_node || "";
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

function connectSSE() {
    const evtSource = new EventSource('/api/stream');
    evtSource.onopen = function() {
        const overlay = document.getElementById('aayu-reconnect-overlay');
        if (overlay) overlay.remove();
    };
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
    evtSource.onerror = function(err) {
        console.error("SSE connection lost. Reconnecting in 3 seconds...", err);
        if (!document.getElementById('aayu-reconnect-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'aayu-reconnect-overlay';
            overlay.style = 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); color: white; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 9999; font-family: monospace;';
            overlay.innerHTML = '<h2>Connection Lost</h2><p>Server restarted or disconnected.</p><p style="color: #aaa; margin-top: 10px;">Reconnecting...</p>';
            document.body.appendChild(overlay);
        }
        evtSource.close();
        setTimeout(connectSSE, 3000);
    };
}
connectSSE();
''')
            
        from runtime.ui.theme import ThemeManager
        with open(os.path.join(self.build_dir, "theme.css"), "w", encoding="utf-8") as f:
            f.write(ThemeManager.instance().generate_css_variables())
            
        import uvicorn
        import threading
        
        print("\n=========================================")
        print("AAYU Async Web Renderer (ASGI) started!")
        print(f"Open in browser: http://localhost:{self.port}")
        print("=========================================\n")
        
        self.thread = threading.Thread(
            target=uvicorn.run, 
            args=(self.asgi_app,), 
            kwargs={"host": "0.0.0.0", "port": self.port, "log_level": "error"},
            daemon=True
        )
        self.thread.start()

    def render(self, tree: RenderTree):
        pass
        
    def process_events(self):
        pass
        
    def present(self):
        pass

    def shutdown(self):
        pass
