const rootEl = document.getElementById('root');
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
        el.className = "fas fa-" + (iconMap[iconName] || "user");
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
            oldEl.classList.remove("fa-" + (iconMap[oldIcon] || "user"));
            oldEl.classList.add("fa-" + (iconMap[newIcon] || "user"));
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
    
    const newStyles = data.styles.join('\n');
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
