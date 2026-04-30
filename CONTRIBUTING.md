# 🤝 Guía de Contribución — DocFlow

Gracias por contribuir a DocFlow. Este documento establece las normas de flujo de trabajo, ramificación y calidad de código necesarias para mantener la integridad del sistema distribuido.

## Tabla de Contenidos

- [Flujo de Trabajo](#flujo-de-trabajo)
- [Estructura de Ramas](#estructura-de-ramas)
- [Convención de Nombres](#convencion-de-nombres)
- [Mensajes de Commit](#mensajes-de-commit)
- [Reglas del Equipo](#reglas-del-equipo)

## Flujo de Trabajo

Este repositorio sigue Git Flow.

**Regla fundamental:** Queda estrictamente prohibido el push directo a `main` o `develop`. Todo cambio debe ingresar vía Pull Request, el cual requiere aprobación obligatoria de al menos un colaborador senior.

## Estructura de Ramas

| Rama | Propósito | Sale de | Mergea en |
|------|-----------|---------|-----------|
| `main` | Producción. Código estable y desplegable. | — | — |
| `develop` | Integración. Convergencia de microservicios. | `main` | — |
| `feature/*` | Nueva funcionalidad o mejora en microservicio. | `develop` | `develop` |
| `release/*` | Ajustes finales antes de producción. | `develop` | `main` y `develop` |
| `hotfix/*` | Corrección crítica de bugs en producción. | `main` | `main` y `develop` |

## Convención de Nombres

Para mantener la trazabilidad en los microservicios:

- `feature/NombreDelMicroservicio_Descripcion`
- `release/vX.Y.Z`
- `hotfix/DescripcionDelBug`

**Ejemplos:**
- `feature/DocService_OllamaIntegration`
- `feature/AuthService_RBAC`
- `feature/WorkflowService_StatusTransitions`
- `hotfix/DocService_FileUploadError`

## Mensajes de Commit (Conventional Commits)

Seguimos una convención estricta para facilitar la auditoría del código:

- `feat(microservicio): descripción corta`      # Nueva funcionalidad
- `fix(microservicio): descripción corta`       # Corrección de bug
- `chore: tareas de mantenimiento/infra`        # Docker, scripts, config
- `docs: cambios en documentación (README)`     # Documentación
- `refactor(microservicio): mejora de código`   # Sin cambios de lógica

**Ejemplos:**
- `feat(doc_service): implement classification logic with Ollama`
- `fix(auth): correct JWT validation in Auth Service`
- `chore(infra): update docker-compose networking`
- `refactor(workflow): optimize state transition queries`

## Reglas del Equipo

- **Aislamiento de dominios:** Los cambios en un microservicio no deben romper la API contractual con otros servicios. Si cambias un endpoint, actualiza la documentación del gateway.
- **Pull Requests:** Todo PR debe incluir una breve descripción de los cambios y validar que los tests de integración pasen correctamente.
- **Vida de las ramas:** Las ramas `feature/*` deben ser de vida corta. Si una tarea toma más de una semana, debe ser sub-dividida en tareas más pequeñas.
- **Limpieza:** Tras mergear un PR, el colaborador es responsable de eliminar la rama tanto local como remotamente.
- **Rebase vs Merge:** 
  - Usa `rebase` para mantener tu rama actualizada con `develop` antes de pushear.
  - Usa `merge --no-ff` al integrar en `main` o `develop` para preservar el historial de trabajo.
- **Offline Compliance:** Cualquier cambio relacionado con la IA debe garantizar que el sistema mantenga su capacidad de ejecución sin conexión (Offline-First).

## Cómo empezar un nuevo Feature

```bash
# 1. Sincronizar develop
git checkout -b develop
git pull origin develop

# 2. Crear rama específica
git checkout -b feature/DocService_PipelineIA

# 3. Desarrollar y commitear (siguiendo convenciones)
git commit -m "feat(doc_service): integrate Ollama classification pipeline"

# 4. Actualizar antes de pushear (evita conflictos)
git fetch origin
git rebase origin/develop

# 5. Push y abrir PR
git push origin feature/DocService_PipelineIA
```