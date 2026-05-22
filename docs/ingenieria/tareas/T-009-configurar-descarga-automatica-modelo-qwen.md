---
id: T-009
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-002
    relationship_type: depends_on
    reason: Depende de la configuración de Docker Compose para configurar descarga de modelo Qwen
---

# T-009: Configurar descarga automática de modelo Qwen 3.5

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 2 horas
**Dependencias**: T-002

## Descripción

Configurar Ollama para descargar automáticamente el modelo Qwen 3.5. Ollama se ejecuta fuera de Docker (en el host o máquina remota), conectado vía Tailscale según ADR-003. La estrategia de descarga automática usa un script que espera a que Ollama esté corriendo y luego descarga el modelo. Qwen 3.5 fue seleccionado según benchmarks de tecnología (SWE-bench 77.2%, performance local 25-30 tokens/seg en Apple Silicon). El threshold de 5 segundos es razonable para prompts simples en desarrollo local.

## Criterios de Aceptación

- [ ] Ollama está instalado y corriendo en el host o máquina remota
- [ ] Ollama es accesible desde contenedores Docker mediante Tailscale
- [ ] Modelo Qwen 3.5 descargado automáticamente en primer startup
- [ ] Comando `ollama list` muestra Qwen 3.5 instalado
- [ ] Comando `ollama run qwen:3.5` responde a prompts de prueba
- [ ] API de Ollama responde a requests HTTP vía Tailscale
- [ ] Latencia de respuesta aceptable (<5 segundos para prompts simples)
- [ ] Documentación de configuración de Tailscale incluida en README

## Script de Inicialización

```bash
#!/bin/bash
# scripts/download-ollama-model.sh

# Esperar a que Ollama esté corriendo (vía Tailscale o localhost)
OLLAMA_URL=${OLLAMA_URL:-http://localhost:11434}

until curl -f $OLLAMA_URL/api/tags; do
  echo "Esperando a que Ollama inicie en $OLLAMA_URL..."
  sleep 5
done

# Descargar modelo Qwen 3.5
echo "Descargando modelo Qwen 3.5..."
curl $OLLAMA_URL/api/pull -d '{"name": "qwen:3.5"}'

echo "Modelo Qwen 3.5 descargado exitosamente"
```

**Nota**: Ollama se ejecuta fuera de Docker según ADR-003. Este script debe ejecutarse manualmente o como parte del setup automatizado (T-011) en el host donde corre Ollama.

## Criterios de Éxito

- Modelo Qwen 3.5 descargado automáticamente en primer startup
- API de Ollama responde con latencia aceptable (<5 segundos para prompts simples)
- Ollama accesible desde contenedores Docker mediante Tailscale
- Script de inicialización funciona sin errores

### Actualización de Modelos

Se usa actualización manual del modelo por el desarrollador.

**Proceso de actualización manual:**

```bash
# Actualizar a la última versión de Qwen 3.5
ollama pull qwen:3.5

# Verificar versión instalada
ollama list
```

**Justificación:** Para desarrollo local, la actualización manual es suficiente. Evita actualizaciones inesperadas que pueden causar interrupciones. El desarrollador actualiza el modelo cuando lo necesite. Actualizaciones automáticas pueden considerarse más adelante si se requiere para producción.

### Validación de Conectividad Tailscale

Se usa validación manual de conectividad Tailscale.

**Comandos de validación:**

1. **Verificar conexión Tailscale:**

```bash
# Verificar que Tailscale está corriendo
tailscale status

# Hacer ping a la máquina remota donde corre Ollama
tailscale ping <machine-name>
```

1. **Verificar que Ollama es accesible vía Tailscale:**

```bash
# Verificar que Ollama responde
curl http://<TAILSCALE_IP>:11434/api/tags

# Verificar que el modelo está instalado
curl http://<TAILSCALE_IP>:11434/api/tags
```

**Justificación:** Para desarrollo local, la validación manual es suficiente. Pruebas automatizadas de conectividad pueden agregarse más adelante si se requiere para CI/CD.

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-005: Ollama Setup
