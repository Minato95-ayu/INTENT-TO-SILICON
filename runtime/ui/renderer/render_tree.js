export class RenderNode {
    constructor(type, props = {}) {
        this.type = type;
        this.props = props;
        this.children = [];
        this.layout = {}; // Calculated by LayoutEngine
        this.styles = {}; // Calculated by StyleEngine
        
        // The actual bridge element (e.g. DOM node)
        this._nativeNode = null;
    }

    addChild(node) {
        this.children.push(node);
    }
}
