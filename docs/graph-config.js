// Configuración y constantes del grafo

export const groupColors = {
    'ESTRATEGIA': '#4A90E2',
    'ARQUITECTURA': '#9B59B6',
    'PRODUCTO': '#E67E22',
    'IMPLEMENTACIÓN': '#27AE60'
};

export const groupBorderColors = {
    'ESTRATEGIA': '#2E5C8A',
    'ARQUITECTURA': '#6C3483',
    'PRODUCTO': '#A04000',
    'IMPLEMENTACIÓN': '#1E8449'
};

export const relationshipColors = {
    'depends_on': '#e74c3c',
    'implements': '#3498db',
    'references': '#95a5a6',
    'explains': '#2ecc71',
    'extends': '#9b59b6',
    'supersedes': '#f39c12',
    'reinforces': '#1abc9c',
    'contradicts': '#e94560'
};

export const relationshipLabels = {
    'depends_on': 'Depende de',
    'implements': 'Implementa',
    'references': 'Referencia',
    'explains': 'Explica',
    'extends': 'Extiende',
    'supersedes': 'Reemplaza',
    'reinforces': 'Refuerza',
    'contradicts': 'Contradice'
};

export const statusLabels = {
    'completed': 'Completado',
    'in-progress': 'En progreso',
    'pending': 'Con gaps/sin rating',
    'missing': 'No existe'
};

export const defaultPhysicsParams = {
    nodeRepulsion: 50000,
    idealEdgeLength: 200,
    gravity: 0.3,
    nodeMass: 1,
    edgeElasticity: 0.45,
    nestingFactor: 0.1,
    numIter: 1000,
    initialTemp: 200,
    coolingFactor: 0.95,
    minTemp: 1
};

export const layoutConfig = {
    name: 'cose',
    animate: true,
    animationDuration: 1000,
    nodeRepulsion: defaultPhysicsParams.nodeRepulsion,
    idealEdgeLength: defaultPhysicsParams.idealEdgeLength,
    gravity: defaultPhysicsParams.gravity,
    nodeMass: defaultPhysicsParams.nodeMass,
    edgeElasticity: defaultPhysicsParams.edgeElasticity,
    nestingFactor: defaultPhysicsParams.nestingFactor,
    numIter: defaultPhysicsParams.numIter,
    initialTemp: defaultPhysicsParams.initialTemp,
    coolingFactor: defaultPhysicsParams.coolingFactor,
    minTemp: defaultPhysicsParams.minTemp,
    nodeOverlap: 20,
    refresh: 20,
    fit: true,
    padding: 30,
    randomize: false,
    componentSpacing: 100,
    nodeDimensionsIncludeLabels: true
};
