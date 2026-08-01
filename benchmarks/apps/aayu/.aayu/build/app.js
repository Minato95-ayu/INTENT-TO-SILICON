const rootEl = document.getElementById('root');
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
