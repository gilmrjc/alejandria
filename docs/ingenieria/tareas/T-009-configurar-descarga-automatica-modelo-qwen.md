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

Configurar Ollama para conectar al servidor externo donde corre el modelo Qwen 3.5. Ollama se ejecuta en un servidor externo (no en el host local), conectado vía Tailscale según ADR-003. No se requiere descarga local del modelo ya que este está pre-instalado en el servidor externo. La configuración consiste en establecer la URL de Ollama (OLLAMA_URL) en las variables de entorno para apuntar al servidor externo. Qwen 3.5 fue seleccionado según benchmarks de tecnología (SWE-bench 77.2%, performance local 25-30 tokens/seg en Apple Silicon). El threshold de 5 segundos es razonable para prompts simples en desarrollo local.

## Criterios de Aceptación

- [ ] Ollama está corriendo en servidor externo accesible vía Tailscale
- [ ] Ollama es accesible desde contenedores Docker mediante Tailscale
- [ ] Variable de entorno OLLAMA_URL configurada para apuntar al servidor externo
- [ ] API de Ollama responde a requests HTTP vía Tailscale
- [ ] Latencia de respuesta aceptable (<5 segundos para prompts simples)
- [ ] Documentación de configuración de Tailscale incluida en README

## Criterios de Éxito

- OLLAMA_URL configurada correctamente para apuntar al servidor externo
- API de Ollama responde con latencia aceptable (<5 segundos para prompts simples)
- Ollama accesible desde contenedores Docker mediante Tailscale
- Modelo Qwen 3.5 disponible en el servidor externo

### Actualización de Modelos

La actualización de modelos se realiza en el servidor externo por el administrador del servidor. No se requiere acción local para actualizar el modelo.

**Justificación:** El modelo corre en un servidor externo administrado centralmente. Los desarrolladores solo necesitan configurar la URL correcta en OLLAMA_URL. Esto simplifica el mantenimiento y asegura consistencia en el modelo usado por todos los desarrolladores.

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
