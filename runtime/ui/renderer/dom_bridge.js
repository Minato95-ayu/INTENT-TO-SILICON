export class DOMBridge {
    constructor(rootElementId) {
        this.rootElement = document.getElementById(rootElementId);
        if (!this.rootElement) {
            throw new Error(`DOMBridge: Root element #${rootElementId} not found.`);
        }
    }

    createElement(tag) {
        return document.createElement(tag);
    }

    createTextNode(text) {
        return document.createTextNode(text);
    }

    appendChild(parent, child) {
        parent.appendChild(child);
    }

    setAttribute(element, key, value) {
        element.setAttribute(key, value);
    }

    setStyle(element, styles) {
        for (const [key, value] of Object.entries(styles)) {
            element.style[key] = value;
        }
    }

    addEventListener(element, event, handler) {
        element.addEventListener(event, handler);
    }

    clearRoot() {
        this.rootElement.innerHTML = '';
    }

    mount(element) {
        this.appendChild(this.rootElement, element);
    }
}
