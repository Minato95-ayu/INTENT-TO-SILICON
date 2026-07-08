import { WidgetFactory } from './widget_factory.js';
import { StyleEngine } from './style_engine.js';
import { LayoutEngine } from './layout_engine.js';
import { EventEngine } from './event_engine.js';
import { DOMBridge } from './dom_bridge.js';

class UIAppRenderer {
    constructor(rootId = 'aayu-root') {
        this.domBridge = new DOMBridge(rootId);
        this.eventEngine = new EventEngine(this.domBridge);
    }

    async boot() {
        console.log("[AAYU UI Engine] Booting...");
        try {
            const res = await fetch('/_ir');
            const appIR = await res.json();
            console.log("[AAYU UI Engine] Received AppIR", appIR);
            
            const pages = appIR.pages || [];
            if (pages.length === 0) {
                console.warn("[AAYU UI Engine] No pages found.");
                return;
            }
            
            this.renderPage(pages[0]);
        } catch (e) {
            console.error("[AAYU UI Engine] Boot failed:", e);
        }
    }

    renderPage(pageData) {
        this.domBridge.clearRoot();
        
        // 1. Build Render Tree from UI IR
        const rootNode = WidgetFactory.build({ type: 'column', children: pageData.children });
        console.log("[AAYU UI Engine] Render Tree Built", rootNode);

        // 2. Compute Layout (Constraints)
        LayoutEngine.computeLayout(rootNode);
        console.log("[AAYU UI Engine] Layout Computed");

        // 3. Compute Styles
        StyleEngine.computeStyles(rootNode);
        console.log("[AAYU UI Engine] Styles Computed");

        // 4. Paint to Bridge
        const nativeRoot = this.paint(rootNode);
        this.domBridge.mount(nativeRoot);
        console.log("[AAYU UI Engine] DOM Bridge Mounted");
    }

    paint(renderNode) {
        let tag = 'div';
        if (renderNode.type === 'heading') tag = 'h1';
        if (renderNode.type === 'button') tag = 'button';
        if (renderNode.type === 'text') tag = 'p';

        const nativeElement = this.domBridge.createElement(tag);
        
        if (renderNode.props.text) {
            const textNode = this.domBridge.createTextNode(renderNode.props.text);
            this.domBridge.appendChild(nativeElement, textNode);
        }

        // Apply pre-computed Layout & Styles
        this.domBridge.setStyle(nativeElement, { ...renderNode.layout, ...renderNode.styles });
        
        // Bind Events
        this.eventEngine.bindEvents(renderNode, nativeElement);

        for (const child of renderNode.children) {
            this.domBridge.appendChild(nativeElement, this.paint(child));
        }

        return nativeElement;
    }
}

// Bootstrap
window.addEventListener('DOMContentLoaded', () => {
    const app = new UIAppRenderer();
    app.boot();
});
