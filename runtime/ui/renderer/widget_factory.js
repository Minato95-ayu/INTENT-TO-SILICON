import { RenderNode } from './render_tree.js';

export class WidgetFactory {
    static build(element) {
        const type = element.type || 'div';
        const props = element.properties || {};
        const node = new RenderNode(type, props);

        const children = element.children || [];
        for (const child of children) {
            node.addChild(WidgetFactory.build(child));
        }

        return node;
    }
}
