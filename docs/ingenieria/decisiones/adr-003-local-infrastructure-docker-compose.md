---
id: ADR-003
type: Architecture Decision Record
rating: 9
rating-phase: document-critique
related:
  - target: ARC-003
    relationship_type: implements
    reason: Implementa la arquitectura general con infraestructura local Docker Compose
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para configuración de PostgreSQL
  - target: ADR-002
    relationship_type: implements
    reason: Implementa el stack unificado Python con servicios de datos orquestados
  - target: STR-003
    relationship_type: implements
    reason: Implementa el Hito 1 - Infraestructura Base del roadmap técnico
---

# ADR-003: Local Infrastructure with Docker Compose

## Context

El Hito 1 del roadmap técnico requiere configurar infraestructura base para desarrollo local con los siguientes componentes:

- PostgreSQL para persistencia de datos
- Redis como broker para jobs y cache
- Qdrant para búsqueda semántica
- Ollama con Qwen 3.5 como LLM provider local (ejecutado fuera de Docker, conectado vía Tailscale)

La fase MVP Bootstrapped opera con recursos limitados (fundador unipersonal, sin inversión externa), por lo que la infraestructura debe ser:

- Simple de configurar y mantener
- Bajo costo operativo (cero costos en desarrollo local)
- Fácil de reproducir en diferentes máquinas
- Adecuada para dogfooding y desarrollo iterativo

## Definiciones de Conceptos

**Dogfooding**: Práctica de usar el propio producto durante su desarrollo para identificar problemas y mejoras desde la perspectiva del usuario. En este contexto, el fundador usa Alejandria para analizar y mejorar su propia documentación técnica, validando el ajuste problema-solución antes de lanzar a usuarios externos.

**MVP Bootstrapped**: Producto Mínimo Viable (MVP) desarrollado con recursos propios del fundador (bootstrapping), sin inversión externa. En este contexto, es una fase de desarrollo con recursos limitados (fundador unipersonal) enfocada en validación del ajuste problema-solución antes de escalar. Sus características son:

- Sin inversión externa
- Infraestructura de bajo costo (cero costos en desarrollo local)
- Prioridad en simplicidad y velocidad de desarrollo
- Validación antes de escalar

**Diferencias entre orquestación local y producción**:

- **Orquestación local (Docker Compose)**: Desarrollo local en máquina del desarrollador, un solo usuario (fundador), sin requisitos de alta disponibilidad, sin monitoreo avanzado, sin escalabilidad horizontal, cero costos operativos.
- **Producción (post-MVP)**: Despliegue en cloud (Kubernetes/Nomad/managed services), múltiples usuarios concurrentes, requisitos de alta disponibilidad (SLAs > 99%), monitoreo/alerting/observabilidad, escalabilidad horizontal, costos operativos de infraestructura cloud.

## Decision

Usar **Docker Compose** para orquestación local de servicios de datos (PostgreSQL, Redis, Qdrant). Ollama se ejecuta fuera de Docker, conectado vía Tailscale.

### Stack de Servicios

Para la configuración detallada de Docker Compose con versiones específicas, puertos, y volumes, ver TRD-001 (RF-001: Docker Compose Configuration).

### Configuración Específica por Servicio

#### PostgreSQL 18.3 Bookworm

- **Versión**: 18.3-bookworm (versión estable con 4 releases, features nuevas: generated columns virtuales, OAuth authentication)
- **Persistencia**: Volume Docker para datos
- **Justificación**: PostgreSQL por integridad ACID y madurez del ecosistema (ver ADR-002). Versión 18.3 seleccionada por estabilidad y features modernas (criterio: latest menos un minor). Imagen Debian elegida sobre Alpine para evitar problemas de compatibilidad (Alpine usa musl libc que puede causar incompatibilidades con ciertas dependencias Python, mientras que Debian usa glibc estándar).

#### Redis 7.4.9 Bookworm

- **Versión**: 7.4.9-bookworm (última versión con licencia BSD3, Redis 8.x usa tri-license RSALv2/SSPLv1/AGPLv3)
- **Persistencia**: AOF (Append Only File) para durabilidad de datos
- **Rol dual**: Broker para Celery y cache del sistema
- **Justificación**: Integración nativa con Celery y bajo overhead. Versión 7.4.9 seleccionada por licencia BSD3 permisiva que evita restricciones de copyleft para posibles modificaciones futuras (Redis se usa solo para cache y jobs, no core del producto). Imagen Debian elegida sobre Alpine para evitar problemas de compatibilidad (Alpine usa musl libc que puede causar incompatibilidades con ciertas dependencias Python, mientras que Debian usa glibc estándar).

#### Qdrant v1.17.1

- **Versión**: v1.17.1 (versión estable probada, v1.18.1 es latest)
- **Persistencia**: Volume Docker para embeddings y colecciones
- **Puertos**: 6333 (HTTP), 6334 (gRPC)
- **Justificación**: Base de datos vectorial open-source con despliegue local simple. Versión pineada para reproducibilidad (criterio: latest menos un minor)

#### Ollama (Fuera de Docker)

- **Ejecución**: Se ejecuta fuera de Docker (en el host o máquina remota)
- **Conectividad**: Accesible desde contenedores Docker mediante Tailscale
- **Modelo**: Qwen 3.5
- **Justificación**: Cero costos de API durante desarrollo local, MCP permite cambio fácil de provider. Ejecución fuera de Docker permite mejor aislamiento y flexibilidad.

### Criterio de Selección de Versiones

El criterio "última versión menos un minor" se aplica a PostgreSQL, Redis y Qdrant. Este enfoque proporciona:

- **Estabilidad**: Las versiones más recientes pueden tener bugs no descubiertos. La versión "última menos un minor" ha tenido tiempo de ser probada en producción por la comunidad.
- **Reproducibilidad**: Versiones específicas aseguran que el entorno sea reproducible en diferentes máquinas y en el tiempo.
- **Balance**: Proporciona funcionalidades modernas sin el riesgo de versiones de vanguardia.

**Riesgos que mitiga**:

- **Bugs de versión reciente**: Evita bugs introducidos en la última versión que aún no han sido reportados o corregidos.
- **Cambios rupturistas**: Versiones recientes pueden tener cambios rupturistas no documentados que rompen el stack.
- **Incompatibilidades**: Dependencias pueden no estar actualizadas para soportar la última versión.

**Ciclo de actualización**:

- Cada 6-12 meses según el roadmap técnico (ver `technical-roadmap.md`)
- Si hay vulnerabilidades críticas en la versión actual
- Si una nueva versión tiene funcionalidades necesarias para el producto
- Cuando la versión actual alcance el fin de vida

### Justificación de Selección de Servicios

**Por qué Redis como broker y cache**:

Según benchmarks de industria, Redis ofrece alta velocidad y simplicidad como broker de mensajes. RabbitMQ es más robusto (confiabilidad, enrutamiento avanzado, confirmaciones de mensajes) pero tiene mayor complejidad y sobrecarga de recursos. Para MVP Bootstrapped con un solo usuario y carga moderada, la simplicidad de Redis supera los beneficios de RabbitMQ. Como cache del sistema, Redis ofrece operaciones en memoria con baja latencia (<10ms) y persistencia AOF para durabilidad. El compromiso de usar el mismo servicio para broker y cache reduce complejidad operacional (un solo servicio) pero puede crear contención bajo alta carga, riesgo aceptable para MVP Bootstrapped.

**Por qué Qdrant vs otras bases vectorales**:

Alternativas consideradas: Pinecone (gestionado, costoso, no permite ajuste de parámetros HNSW), Weaviate (open-source, búsqueda híbrida nativa), pgvector (extensión de Postgres, buena opción pero requiere Postgres dedicado), Milvus (orientado a enterprise, escala de miles de millones). Qdrant se seleccionó por su rendimiento (mantiene latencias p50 <5ms hasta 1M vectores con alta recuperación, más que suficiente para MVP Bootstrapped con escala local), facilidad de gestión en ambientes locales (despliegue simple con Docker, API REST y gRPC intuitiva, buena documentación), y ser open-source sin costos para desarrollo local. pgvector con Neon es una alternativa interesante (un solo database para todo) pero requiere migración a Postgres serverless fuera del alcance actual.

**Por qué Ollama vs otros proveedores LLM locales**:

Alternativas consideradas: llama.cpp (máximo control, requiere compilación manual), vLLM (rendimiento de producción, 3-5x más usuarios concurrentes, requiere GPUs NVIDIA), LocalAI (endpoint compatible con OpenAI). Según benchmarks 2026, Ollama es "Docker para LLMs" - un comando para instalar, uno para ejecutar. API compatible con OpenAI, maneja descarga y serving automáticamente. Ideal para desarrollo local y dogfooding con un solo usuario. Para producción con múltiples usuarios concurrentes, vLLM sería mejor opción (3-5x rendimiento), pero eso es post-MVP.

## Justification

### Por qué Docker Compose

#### Simplicidad operacional

- Un solo comando (`docker-compose up`) levanta todos los servicios
- Configuración declarativa en YAML fácil de versionar
- Elimina necesidad de instalar servicios nativamente en cada máquina de desarrollo

#### Reproducibilidad

- Mismo entorno en todas las máquinas de desarrollo
- Versiones específicas de cada servicio (no drift de versiones)
- Aislamiento de dependencias (no conflictos con servicios del host)

#### Adecuado para MVP Bootstrapped

- Cero costo operativo (no requiere servicios cloud)
- Baja complejidad operacional (sin Kubernetes/Nomad)
- Suficiente para desarrollo local y dogfooding
- Escalable a producción post-MVP con migración a orquestación cloud

#### Alineación con principios técnicos

- **Baja Fricción**: Configuración simple con un comando, baja curva de aprendizaje
- **Calidad Automática**: Entorno consistente reduce bugs de "funciona en mi máquina"

### Por qué no alternativas consideradas

#### Kubernetes/Nomad local (minikube, kind, nomad-dev)

- Rechazado: Complejidad excesiva para fase MVP bootstrapped
- Rechazado: Overhead operacional innecesario para desarrollo local
- Rechazado: Learning curve steep para fundador unipersonal

#### Instalación nativa de servicios

- Rechazado: Difícil de reproducir across diferentes máquinas
- Rechazado: Conflictos potenciales con servicios existentes del host
- Rechazado: Diferentes versiones según OS (macOS vs Linux)

#### Docker Swarm

- Rechazado: Menor ecosistema y comunidad que Docker Compose
- Rechazado: Docker Compose es suficiente para orquestación local
- Rechazado: Swarm está en modo mantenimiento, Compose es el estándar actual

#### Podman

- Rechazado: Alternativa a Docker con mejor seguridad (rootless), pero menor ecosistema y herramientas de desarrollo
- Rechazado: Docker Desktop tiene mejor integración con macOS/Windows y mayor comunidad

#### Rancher Desktop

- Rechazado: Ofrece Kubernetes local, pero añade complejidad innecesaria para MVP Bootstrapped que solo requiere orquestación simple de contenedores

#### Lima/Colima

- Rechazado: Alternativas ligeras para macOS, pero Docker Desktop es el estándar de facto con mejor documentación y soporte

#### Kubernetes local (minikube, kind)

- Rechazado: Complejidad excesiva para desarrollo local de MVP Bootstrapped

**Decisión**: Docker Compose es suficiente para MVP Bootstrapped. Si hay problemas de compatibilidad o requerimientos específicos en el futuro, se evaluarán alternativas. El criterio de decisión es simplicidad y ecosistema maduro. Docker es el estándar de desarrollo.

## Consecuencias

### Positivas

- **Configuración rápida**: Nuevo desarrollador puede tener el stack corriendo en menos de 15 minutos
- **Cero costos**: Desarrollo local sin gastos de servicios cloud
- **Versionado de infraestructura**: Archivo Docker Compose versionado en Git
- **Facilidad de depuración**: Logs de todos los servicios en un lugar (`docker-compose logs`)
- **Aislamiento**: Servicios aislados del host, no contaminan el sistema

### Negativas

- **Sobrecarga de Docker**: Requiere Docker Desktop instalado (~2GB en disco)
- **Rendimiento**: Ligera sobrecarga de virtualización vs nativo (aceptable para desarrollo)
- **Curva de aprendizaje**: El equipo necesita aprender Docker Compose básico
- **Limitación a desarrollo local**: No es adecuado para producción (requiere migración post-MVP)

### Mitigación

- **Documentación de configuración**: Guía paso a paso para instalar Docker Desktop y levantar el stack
- **Scripts de ayuda**: Script `./scripts/dev-setup.sh` para automatizar la configuración inicial
- **Documentación de solución de problemas**: Sección de problemas comunes y soluciones
- **Plan de migración a producción**: Documentar estrategia de migración a Kubernetes/Nomad post-MVP

## Consideraciones de Seguridad

Esta sección describe el enfoque de seguridad específico para Docker Compose local. Para el modelo de seguridad completo del stack (autenticación, autorización, cifrado, seguridad MCP/LLM), ver `technology-stack.md` sección "Modelo de Seguridad". Consideraciones de seguridad avanzadas (non-root, límites de recursos, backups automatizados) se definirán en fase post-MVP.

### Gestión de Secrets (MVP Bootstrapped)

Usar variables de entorno en Docker Compose (archivo `.env`) para secrets. El archivo `.env` debe estar en `.gitignore` para no confirmar secrets en el repositorio. Documentar `.env.example` con la estructura de variables requeridas.

### Políticas de Red (MVP Bootstrapped)

Docker Compose crea una red bridge por defecto que aísla servicios del host. Los servicios se comunican entre sí por nombres de servicio (ej: `postgresql:5432`). Solo los puertos explícitamente mapeados (`ports: ["5432:5432"]`) son accesibles desde el host.

### Endurecimiento de Contenedores (MVP Bootstrapped)

Usar imágenes Alpine (ya implementado: `postgres:18.3-alpine`, `redis:7.4.9-alpine`) para reducir la superficie de ataque.

### Backup y Recuperación de Desastres (MVP Bootstrapped)

- **PostgreSQL**: Volume Docker persiste datos; backup manual con `pg_dump` cuando sea necesario
- **Redis**: AOF (Append Only File) ya configurado para durabilidad
- **Qdrant**: Volume Docker persiste embeddings
- **Ollama**: Volume Docker persiste modelos descargados

## Requisitos de Hardware y Rendimiento

Esta sección describe los requisitos de hardware para desarrollo local. Límites de recursos por servicio, métricas de rendimiento específicas, y estrategia de monitoreo detallada se definirán en fase post-MVP. Para MVP Bootstrapped, el foco es funcionalidad básica sin optimización de recursos.

### Requisitos de hardware mínimos (desarrollo local)

- **CPU**: 4 núcleos mínimo (8 núcleos recomendado para Ollama + Qdrant + desarrollo)
- **RAM**: 16GB mínimo (32GB recomendado para Ollama con Qwen 3.5)
- **Almacenamiento**: 20GB para imágenes Docker + volumes (50GB recomendado para crecimiento)
- **SO**: Cualquier sistema operativo capaz de ejecutar Docker Desktop (macOS, Linux, Windows con WSL2)

**Nota**: Para requisitos detallados por componente, ver `technology-stack.md` sección "Requisitos de Recursos".

## Configuración de Desarrollo Local

### Configuración de Variables de Entorno

Crear archivo `.env` en el directorio del proyecto:

```env
POSTGRES_PASSWORD=your_secure_password_here
```

El archivo `.env` debe estar en `.gitignore` (mejor práctica de seguridad).

### Notas sobre componentes no implementados aún

- **Ollama**: Se ejecuta fuera de Docker (en el host o máquina remota), conectado mediante Tailscale para ser accesible desde los contenedores Docker. Docker Compose no gestiona Ollama como servicio.

**Nota**: Se asume que Docker Desktop ya está instalado. Docker Compose automatiza la descarga de imágenes, ejecución y montaje de volumes.

## Estrategia de Migración a Producción (Post-MVP)

Esta decisión aplica específicamente a la fase MVP Bootstrapped. Para producción post-MVP, se evaluará la migración a orquestación cloud cuando se cumplan los siguientes criterios:

### Criterios de transición a orquestación cloud

1. **Validación del ajuste problema-solución**: El sistema debe demostrar que resuelve un problema real para usuarios. Este criterio se alinea con la estrategia del MVP Bootstrapped descrita en `technical-roadmap.md` donde las funcionalidades post-MVP dependen de la validación del ajuste problema-solución.

2. **Escalabilidad horizontal requerida**: Cuando la carga de usuarios exceda la capacidad de una sola máquina. Docker Compose está diseñado para orquestación local en una sola máquina; cuando se requiera escalar horizontalmente, será necesario migrar a orquestación cloud.

### Alternativas para producción

Las alternativas específicas de producción (Kubernetes, Nomad, managed services) y la estrategia detallada de migración se definirán cuando se alcance el punto de transición post-MVP. Actualmente el foco es desarrollo local con Docker Compose, y definir alternativas de producción sin contexto real de requisitos sería especulativo.

## Referencias

- **[technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Hito 1 - Infraestructura Base
- **[technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico y decisiones
- **[database-schema-design.md](../arquitectura/database-schema-design.md)**: Diseño conceptual de schema de PostgreSQL
- **[ADR-002](adr-002-python-unified-stack.md)**: Stack unificado en Python
- **[ADR-001](adr-001-mcp-abstraction-layer.md)**: MCP como capa de abstracción
