export class StyleEngine {
    static computeStyles(renderNode) {
        const styles = {};
        
        // Translates AAYU props to standard CSS constraints.
        // In a non-DOM bridge (like Canvas), these would be interpreted directly by the painter.
        
        if (renderNode.type === 'button') {
            styles['padding'] = '10px 20px';
            styles['background'] = 'var(--primary, #007bff)';
            styles['color'] = 'white';
            styles['border'] = 'none';
            styles['borderRadius'] = '4px';
            styles['cursor'] = 'pointer';
        }
        
        // Basic mapping of raw props to styles
        if (renderNode.props.padding) {
            styles['padding'] = `${renderNode.props.padding}px`;
        }
        if (renderNode.props.color) {
            styles['color'] = renderNode.props.color;
        }
        
        renderNode.styles = styles;
        
        for (const child of renderNode.children) {
            StyleEngine.computeStyles(child);
        }
    }
}
