# Configuración del GitHub Project y Tablero Ágil

> **Estado real en GitHub:** El código y las ramas están subidos en https://github.com/andressantiagomeloaguirre67-sys/Hackathon. La creación del Project y de los Issues en la interfaz de GitHub se encuentra **pendiente** de ejecutar con `gh auth login` o desde la interfaz web de GitHub.

## 1. Estructura del GitHub Project

* **Repositorio:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon
* **URL de Projects del repositorio:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/projects
* **Nombre del Proyecto:** `Directorio Cultural Colombia - Sprint 1`
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

## 2. Estado Real del Tablero (según la DoD actual)

| Issue | Título | Priority | Rama en GitHub | Estado real (`Status`) | Motivo del estado |
|---|---|---|---|---|---|
| **#1** | Consulta de espacios culturales reales y manejo resiliente de datos | `High` | `feature/cultural-spaces-listing` | `In Progress` / Pendiente crear en GitHub | Código implementado y subido a `origin`, pendiente creación del Issue en GitHub. |
| **#2** | Búsqueda y filtrado seguro por municipio, departamento, tipo de espacio y nombre | `High` | `feature/search-and-filter` y `feature/improve-empty-states` | `In Review` / Pendiente revisión de PR | La rama `feature/improve-empty-states` está subida y pendiente de revisión y fusión del PR (`Refs #2`). |
| **#3** | Resumen estadístico rápido de los resultados consultados | `Medium` | `feature/results-summary` | `In Progress` / Pendiente crear en GitHub | Código y pruebas implementados y subidos a `origin`, pendiente creación del Issue en GitHub. |
