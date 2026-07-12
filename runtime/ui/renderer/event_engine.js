export class EventEngine {
    constructor(domBridge) {
        this.domBridge = domBridge;
    }

    bindEvents(renderNode, nativeElement) {
        // e.g. onClick from AAYU IR
        if (renderNode.props.onClick) {
            this.domBridge.addEventListener(nativeElement, 'click', (e) => {
                console.log(`[EventEngine] Click captured for action: ${renderNode.props.onClick}`);
                // Future: Dispatch action to AAYU State Runtime
            });
        }
    }
}
