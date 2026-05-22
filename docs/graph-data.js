// Carga y gestión de datos del grafo

export class GraphDataLoader {
    constructor() {
        this.graphData = { nodes: [], edges: [] };
    }

    async load() {
        try {
            const response = await fetch(`./dependency-graph.json?t=${new Date().getTime()}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const rawData = await response.text();
            const parsedData = JSON.parse(rawData);
            
            this.graphData = this.validateData(parsedData);
            console.log(`Grafo cargado: ${this.graphData.nodes.length} nodos, ${this.graphData.edges.length} edges`);
            return this.graphData;
        } catch (error) {
            console.error('Error cargando grafo:', error);
            this.graphData = { nodes: [], edges: [] };
            return this.graphData;
        }
    }

    validateData(data) {
        if (!data || typeof data !== 'object') {
            console.warn('Datos inválidos: se esperaba un objeto');
            return { nodes: [], edges: [] };
        }

        if (!Array.isArray(data.nodes)) {
            console.warn('Datos inválidos: nodes no es un array');
            data.nodes = [];
        }

        if (!Array.isArray(data.edges)) {
            console.warn('Datos inválidos: edges no es un array');
            data.edges = [];
        }

        // Validar nodos
        const validNodes = data.nodes.filter(node => {
            if (!node || typeof node !== 'object') {
                console.warn('Nodo inválido encontrado y omitido');
                return false;
            }
            if (!node.id) {
                console.warn('Nodo sin id omitido');
                return false;
            }
            return true;
        });

        // Validar edges
        const validEdges = data.edges.filter(edge => {
            if (!edge || typeof edge !== 'object') {
                console.warn('Edge inválido encontrado y omitido');
                return false;
            }
            if (!edge.source || !edge.target) {
                console.warn('Edge sin source o target omitido');
                return false;
            }
            return true;
        });

        if (validNodes.length !== data.nodes.length) {
            console.warn(`Se omitieron ${data.nodes.length - validNodes.length} nodos inválidos`);
        }

        if (validEdges.length !== data.edges.length) {
            console.warn(`Se omitieron ${data.edges.length - validEdges.length} edges inválidos`);
        }

        return {
            nodes: validNodes,
            edges: validEdges
        };
    }

    getData() {
        return this.graphData;
    }

    getStats() {
        const nodes = this.graphData.nodes;
        return {
            total: nodes.length,
            estrategia: nodes.filter(n => n.group === 'ESTRATEGIA').length,
            arquitectura: nodes.filter(n => n.group === 'ARQUITECTURA').length,
            producto: nodes.filter(n => n.group === 'PRODUCTO').length,
            implementacion: nodes.filter(n => n.group === 'IMPLEMENTACIÓN').length
        };
    }
}
