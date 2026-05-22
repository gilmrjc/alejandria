// Gestión de física y layout del grafo

import { layoutConfig } from './graph-config.js';

export class PhysicsManager {
    constructor(baseConfig = layoutConfig) {
        this.baseConfig = { ...baseConfig };
        this.currentConfig = { ...baseConfig };
        this.listeners = [];
    }

    getConfig() {
        return { ...this.currentConfig };
    }

    updateParam(param, value) {
        this.currentConfig[param] = parseFloat(value);
        this.notify('physicsChanged', { param, value: this.currentConfig[param] });
    }

    adjustRepulsionParams(targetValue) {
        const repulsionRatio = targetValue / this.baseConfig.nodeRepulsion;
        this.currentConfig.idealEdgeLength = this.baseConfig.idealEdgeLength * repulsionRatio;
        this.currentConfig.nodeOverlap = 20 * repulsionRatio;
        this.currentConfig.componentSpacing = 100 * repulsionRatio;
        this.currentConfig.numIter = Math.min(2500, 1000 * repulsionRatio);
        this.currentConfig.edgeElasticity = Math.max(0.1, 0.45 / repulsionRatio);
    }

    interpolateParam(param, targetValue, steps = 10, stepDuration = 50) {
        const currentValue = this.currentConfig[param];
        const stepSize = (targetValue - currentValue) / steps;
        let currentStep = 0;

        return new Promise((resolve) => {
            const interpolate = () => {
                if (currentStep < steps) {
                    currentStep++;
                    this.currentConfig[param] = currentValue + (stepSize * currentStep);
                    this.notify('physicsInterpolated', this.getConfig());
                    setTimeout(interpolate, stepDuration);
                } else {
                    this.currentConfig[param] = targetValue;
                    this.notify('physicsChanged', { param, value: targetValue });
                    resolve();
                }
            };
            interpolate();
        });
    }

    reset() {
        this.currentConfig = { ...this.baseConfig };
        this.notify('physicsReset', this.getConfig());
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
