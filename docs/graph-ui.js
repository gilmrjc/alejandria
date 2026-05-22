// Manejo de UI y eventos del grafo

import { relationshipLabels, statusLabels, defaultPhysicsParams } from './graph-config.js';

export class GraphUI {
    constructor(visualizer, dataLoader) {
        this.visualizer = visualizer;
        this.dataLoader = dataLoader;
        this.filters = {
            'ESTRATEGIA': true,
            'ARQUITECTURA': true,
            'PRODUCTO': true,
            'IMPLEMENTACIÓN': true
        };
        this.listeners = [];
    }

    setupEventListeners() {
        const cy = this.visualizer.getCy();

        // Click en nodo
        cy.on('tap', 'node', (evt) => this.handleNodeClick(evt));

        // Click en arista
        cy.on('tap', 'edge', (evt) => this.handleEdgeClick(evt));

        // Click en fondo
        cy.on('tap', (evt) => {
            if (evt.target === cy) {
                this.handleBackgroundClick();
            }
        });
    }

    handleNodeClick(evt) {
        const node = evt.target;
        const cy = this.visualizer.getCy();
        const data = node.data();

        cy.edges().style('width', 2);
        cy.nodes().unselect();
        node.select();
        const connectedEdges = node.connectedEdges();
        connectedEdges.style('width', 4);
        node.neighborhood().nodes().select();

        const relationships = {};
        connectedEdges.forEach(edge => {
            const relType = edge.data('relationship_type');
            relationships[relType] = (relationships[relType] || 0) + 1;
        });

        const relHtml = Object.entries(relationships)
            .map(([type, count]) => `<p><span class="label">${relationshipLabels[type] || type}:</span> ${count}</p>`)
            .join('');

        this.updateNodeInfo(`
            <h3>Información del Nodo</h3>
            <p><span class="label">Archivo:</span> ${data.label}</p>
            <p><span class="label">Estado:</span> ${statusLabels[data.status]}</p>
            <p><span class="label">Rating:</span> ${data.rating || 'N/A'}</p>
            <p><span class="label">Grupo:</span> ${data.group}</p>
            <p><span class="label">Hito:</span> ${data.milestone || 'N/A'}</p>
            <hr style="margin: 10px 0; border-color: #0f3460;">
            <p><span class="label">Relaciones (${connectedEdges.length}):</span></p>
            ${relHtml || '<p>Ninguna</p>'}
        `);
    }

    handleEdgeClick(evt) {
        const edge = evt.target;
        const cy = this.visualizer.getCy();
        const data = edge.data();

        cy.elements().unselect();
        edge.select();
        edge.source().select();
        edge.target().select();

        this.updateNodeInfo(`
            <h3>Información de Relación</h3>
            <p><span class="label">Tipo:</span> ${relationshipLabels[data.relationship_type] || data.relationship_type}</p>
            <p><span class="label">Origen:</span> ${edge.source().data('label')}</p>
            <p><span class="label">Destino:</span> ${edge.target().data('label')}</p>
            ${data.reason ? `<p><span class="label">Razón:</span> ${data.reason}</p>` : ''}
        `);
    }

    handleBackgroundClick() {
        const cy = this.visualizer.getCy();
        cy.edges().style({ 'line-color': '#0f3460', 'target-arrow-color': '#0f3460', 'width': 2 });
        cy.elements().unselect();
        this.updateNodeInfo('');
    }

    updateNodeInfo(html) {
        document.getElementById('node-info').innerHTML = html;
    }

    updateStats() {
        const stats = this.dataLoader.getStats();
        document.getElementById('total-nodes').textContent = stats.total;
        document.getElementById('estrategia-nodes').textContent = stats.estrategia;
        document.getElementById('arquitectura-nodes').textContent = stats.arquitectura;
        document.getElementById('producto-nodes').textContent = stats.producto;
        document.getElementById('implementacion-nodes').textContent = stats.implementacion;
    }

    setupPhysicsControls() {
        const repulsionInput = document.querySelector('input[data-param="nodeRepulsion"]');
        const gravityInput = document.querySelector('input[data-param="gravity"]');
        
        if (repulsionInput) {
            const config = this.visualizer.getPhysicsManager().getConfig();
            repulsionInput.value = config.nodeRepulsion;
            const repulsionValue = document.getElementById('repulsion-value');
            if (repulsionValue) repulsionValue.textContent = config.nodeRepulsion;
            
            repulsionInput.addEventListener('input', (e) => {
                const value = e.target.value;
                const repulsionValue = document.getElementById('repulsion-value');
                if (repulsionValue) repulsionValue.textContent = value;
                this.visualizer.updatePhysics('nodeRepulsion', value);
            });
        }
        
        if (gravityInput) {
            const config = this.visualizer.getPhysicsManager().getConfig();
            gravityInput.value = config.gravity;
            const gravityValue = document.getElementById('gravity-value');
            if (gravityValue) gravityValue.textContent = config.gravity;
            
            gravityInput.addEventListener('input', (e) => {
                const value = e.target.value;
                const gravityValue = document.getElementById('gravity-value');
                if (gravityValue) gravityValue.textContent = value;
                this.visualizer.updatePhysics('gravity', value);
            });
        }
    }

    setupFilterControls() {
        const filterCheckboxes = document.querySelectorAll('.filter-checkbox input');
        filterCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const group = e.target.value;
                this.filters[group] = e.target.checked;
                this.visualizer.toggleFilter(group, this.filters[group]);
                this.notify('filterChanged', { group, visible: this.filters[group] });
            });
        });
    }

    setupControlButtons() {
        const resetBtn = document.querySelector('button[data-action="resetLayout"]');
        const fitBtn = document.querySelector('button[data-action="fitToScreen"]');
        const centerBtn = document.querySelector('button[data-action="centerGraph"]');
        const expandBtn = document.querySelector('button[data-action="expandGraph"]');
        const compactBtn = document.querySelector('button[data-action="compactGraph"]');
        
        if (resetBtn) resetBtn.addEventListener('click', () => this.visualizer.resetLayout());
        if (fitBtn) fitBtn.addEventListener('click', () => this.visualizer.fitToScreen());
        if (centerBtn) centerBtn.addEventListener('click', () => this.visualizer.centerGraph());
        if (expandBtn) expandBtn.addEventListener('click', () => this.visualizer.expandGraph());
        if (compactBtn) compactBtn.addEventListener('click', () => this.visualizer.compactGraph());
    }

    initialize() {
        this.setupEventListeners();
        this.setupControlButtons();
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
}
