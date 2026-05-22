// Visualización del grafo con Cytoscape

import { PhysicsManager } from './graph-physics-manager.js';
import { StyleManager } from './graph-style-manager.js';
import { layoutConfig } from './graph-config.js';

export class GraphVisualizer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.cy = null;
        this.physicsManager = new PhysicsManager(layoutConfig);
        this.styleManager = new StyleManager();
        this.listeners = [];
        this.baseRepulsion = layoutConfig.nodeRepulsion;
        this.baseGravity = layoutConfig.gravity;
        this.baseEdgeLength = layoutConfig.idealEdgeLength;
    }

    initialize(graphData) {
        console.log(`Inicializando grafo: ${graphData.nodes.length} nodos, ${graphData.edges.length} edges`);
        
        this.cy = cytoscape({
            container: this.container,
            elements: this.buildElements(graphData),
            style: this.styleManager.buildStyles(),
            layout: this.physicsManager.getConfig()
        });

        this.setupPhysicsListeners();
        return this.cy;
    }

    buildElements(graphData) {
        // Calcular in-degree para cada nodo
        const inDegree = {};
        graphData.edges.forEach(edge => {
            inDegree[edge.target] = (inDegree[edge.target] || 0) + 1;
        });

        return [
            ...graphData.nodes.map(node => ({
                data: {
                    id: node.id,
                    label: node.label,
                    status: node.status,
                    rating: node.rating,
                    group: node.group,
                    milestone: node.milestone,
                    inDegree: inDegree[node.id] || 0
                }
            })),
            ...graphData.edges.map(edge => ({
                data: {
                    source: edge.source,
                    target: edge.target,
                    relationship_type: edge.relationship_type || 'depends_on',
                    reason: edge.reason || ''
                }
            }))
        ];
    }

    setupPhysicsListeners() {
        this.physicsManager.on('physicsInterpolated', (config) => {
            this.cy.layout({
                ...config,
                randomize: false,
                padding: 50,
                animate: true,
                animationDuration: 50
            }).run();
        });

        this.physicsManager.on('physicsChanged', ({ param, value }) => {
            if (param === 'nodeRepulsion') this.applyNodeSpacing();
            if (param === 'gravity') {
                this.applyGravitySpacing();
                this.updateNodeSizesByGravity();
            }
            this.applyAutoZoom();
        });
    }

    resetLayout() {
        this.physicsManager.reset();
        this.cy.layout({
            ...this.physicsManager.getConfig(),
            randomize: false
        }).run();
    }

    fitToScreen() {
        this.cy.fit(null, 50);
    }

    centerGraph() {
        this.cy.center();
    }

    calculateZoomFactor() {
        const config = this.physicsManager.getConfig();
        const repulsionRatio = config.nodeRepulsion / this.baseRepulsion;
        const gravityRatio = config.gravity / this.baseGravity;
        const repulsionEffect = Math.pow(repulsionRatio, 0.3);
        const gravityFactor = 1 / (gravityRatio * 0.4 + 0.6);
        const zoomFactor = gravityFactor / repulsionEffect;
        return Math.max(0.5, Math.min(2.5, zoomFactor));
    }

    measureEdgeLengths() {
        const edges = this.cy.edges();
        let totalLength = 0;
        let count = 0;

        edges.forEach(edge => {
            const source = edge.source();
            const target = edge.target();
            const dx = target.position('x') - source.position('x');
            const dy = target.position('y') - source.position('y');
            totalLength += Math.sqrt(dx * dx + dy * dy);
            count++;
        });

        return count > 0 ? totalLength / count : 0;
    }

    applyAutoZoom() {
        this.cy.animate({
            zoom: this.cy.zoom() * this.calculateZoomFactor()
        }, {
            duration: 300,
            easing: 'ease-out'
        });
    }

    applyNodeSpacing() {
        const config = this.physicsManager.getConfig();
        this.applySpacingFactor(Math.pow(config.nodeRepulsion / this.baseRepulsion, 1.8));
    }

    applyGravitySpacing() {
        const config = this.physicsManager.getConfig();
        const gravityRatio = config.gravity / this.baseGravity;
        this.applySpacingFactor(1 / Math.pow(gravityRatio, 1.5));
    }

    applySpacingFactor(spacingFactor) {
        const extent = this.cy.extent();
        const center = {
            x: (extent.x1 + extent.x2) / 2,
            y: (extent.y1 + extent.y2) / 2
        };
        this.cy.nodes().forEach(node => {
            const pos = node.position();
            node.position({
                x: center.x + (pos.x - center.x) * spacingFactor,
                y: center.y + (pos.y - center.y) * spacingFactor
            });
        });
    }

    updateNodeSizesByGravity() {
        const config = this.physicsManager.getConfig();
        const sizeMultiplier = Math.max(0.5, Math.min(2, config.gravity / this.baseGravity));
        this.cy.nodes().forEach(node => {
            const inDegree = node.data('inDegree') || 0;
            const baseSize = 40 + Math.min(inDegree, 10) * 6;
            const newSize = baseSize * sizeMultiplier;
            node.style({ width: newSize, height: newSize });
        });
    }

    updatePhysics(param, value) {
        const targetValue = parseFloat(value);
        
        if (param === 'nodeRepulsion') {
            this.physicsManager.adjustRepulsionParams(targetValue);
        }

        if (this.physicsTimeout) clearTimeout(this.physicsTimeout);
        this.physicsTimeout = setTimeout(() => {
            this.physicsManager.interpolateParam(param, targetValue);
        }, 300);
    }

    toggleFilter(group, visible) {
        this.cy.nodes().forEach(node => {
            if (node.data('group') === group) {
                node.style('display', visible ? 'element' : 'none');
            }
        });
    }

    getCy() {
        return this.cy;
    }

    expandGraph() {
        const config = this.physicsManager.getConfig();
        this.updatePhysics('nodeRepulsion', config.nodeRepulsion * 1.5);
    }

    compactGraph() {
        const config = this.physicsManager.getConfig();
        this.updatePhysics('nodeRepulsion', config.nodeRepulsion * 0.7);
    }

    // Observer pattern
    on(event, callback) {
        this.listeners.push({ event, callback });
    }

    notify(event, data) {
        this.listeners
            .filter(l => l.event === event)
            .forEach(l => l.callback(data));
    }

    getPhysicsManager() {
        return this.physicsManager;
    }

    getStyleManager() {
        return this.styleManager;
    }
}
