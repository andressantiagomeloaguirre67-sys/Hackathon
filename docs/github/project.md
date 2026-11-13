# Configuración del GitHub Project y Tablero Ágil

> **Nota de transparencia:** En este entorno local no se encuentra instalado el cliente `gh` (`which gh` no disponible) ni hay un control remoto configurado en GitHub. Siguiendo las reglas del proyecto, se dejan aquí todos los textos estructurados listos para copiar a mano en GitHub Projects e Issues, manteniendo este tablero sincronizado con el estado real tras verificar la Definición de Hecho (DoD).

## 1. Estructura del GitHub Project

* **Nombre del Proyecto:** `Directorio Cultural Colombia - Sprint 1`
* **Plantilla sugerida:** Board / Table
* **Campo de estado (`Status`):**
  1. `Backlog`
  2. `Ready`
  3. `In Progress`
  4. `In Review`
  5. `Done`
* **Campo personalizado (`Priority` - Single Select):**
  * `High`
  * `Medium`
  * `Low`

---

## 2. Estado Actual del Tablero (Project Board)

| Issue | Título | Priority | Rama asociada | PR asociado | Estado (`Status`) |
|---|---|---|---|---|---|
| **#1** | Consulta de espacios culturales reales y manejo resiliente de datos | `High` | `feature/cultural-spaces-listing` | PR #1 (`Refs #1`) | `Done` |
| **#2** | Búsqueda y filtrado seguro por municipio, departamento, tipo de espacio y nombre | `High` | `feature/search-and-filter` | PR #2 (`Refs #2`) | `Done` |
| **#3** | Resumen estadístico rápido de los resultados consultados | `Medium` | `feature/results-summary` | PR #3 (`Refs #3`) | `Done` |
