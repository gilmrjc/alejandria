// Gestión de estilos del grafo

import { groupColors, groupBorderColors, relationshipColors } from './graph-config.js';

export class StyleManager {
    constructor() {
        this.customStyles = new Map();
    }

    buildStyles() {
        const styles = [
            this.buildBaseNodeStyle(),
            ...this.buildGroupStyles(),
            this.buildMissingNodeStyle(),
            this.buildSelectedNodeStyle(),
            this.buildBaseEdgeStyle(),
            ...this.buildRelationshipStyles(),
            this.buildSelectedEdgeStyle()
        ];

        return styles;
    }

    buildBaseNodeStyle() {
        return {
            selector: 'node',
            style: {
                'background-color': 'data(group)',
                'border-color': 'data(group)',
                'border-width': 3,
                'label': 'data(label)',
                'color': '#ffffff',
                'text-valign': 'center',
                'text-halign': 'center',
                'font-size': '10px',
                'font-weight': 'bold',
                'width': 'mapData(inDegree, 0, 10, 40, 100)',
                'height': 'mapData(inDegree, 0, 10, 40, 100)',
                'text-wrap': 'wrap',
                'text-max-width': '80px',
                'shape': 'ellipse',
                'transition-property': 'background-color, border-color, border-width, width, height, opacity',
                'transition-duration': '0.3s',
                'transition-timing-function': 'ease-out'
            }
        };
    }

    buildGroupStyles() {
        return Object.entries(groupColors).map(([group, color]) => ({
            selector: `node[group="${group}"]`,
            style: {
                'background-color': color,
                'border-color': groupBorderColors[group]
            }
        }));
    }

    buildMissingNodeStyle() {
        return {
            selector: 'node[status="missing"]',
            style: {
                'border-style': 'dashed'
            }
        };
    }

    buildSelectedNodeStyle() {
        return {
            selector: 'node:selected',
            style: {
                'border-width': 5,
                'border-color': '#e94560'
            }
        };
    }

    buildBaseEdgeStyle() {
        return {
            selector: 'edge',
            style: {
                'width': 2,
                'line-color': 'data(relationship_type)',
                'target-arrow-color': 'data(relationship_type)',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'line-style': 'solid',
                'transition-property': 'line-color, target-arrow-color, width, opacity',
                'transition-duration': '0.3s',
                'transition-timing-function': 'ease-out'
            }
        };
    }

    buildRelationshipStyles() {
        return Object.entries(relationshipColors).map(([type, color]) => {
            const baseStyle = {
                selector: `edge[relationship_type="${type}"]`,
                style: {
                    'line-color': color,
                    'target-arrow-color': color
                }
            };

            if (type === 'references') {
                baseStyle.style['line-style'] = 'dashed';
            }
            if (type === 'contradicts') {
                baseStyle.style['width'] = 3;
            }

            return baseStyle;
        });
    }

    buildSelectedEdgeStyle() {
        return {
            selector: 'edge:selected',
            style: {
                'line-color': '#e94560',
                'target-arrow-color': '#e94560',
                'width': 8
            }
        };
    }

    addCustomStyle(selector, style) {
        this.customStyles.set(selector, style);
    }

    removeCustomStyle(selector) {
        this.customStyles.delete(selector);
    }

    getCustomStyles() {
        return Array.from(this.customStyles.entries()).map(([selector, style]) => ({
            selector,
            style
        }));
    }
}
