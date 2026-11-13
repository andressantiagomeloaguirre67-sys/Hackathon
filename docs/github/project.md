# Configuración del GitHub Project y Tablero Ágil Completo

* **Repositorio:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon
* **URL de Projects del repositorio:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/projects
* **Catálogo detallado de las 8 Historias de Usuario (listo para copiar):** [`docs/HISTORIADEUSUARIO_ISSUES.md`](../HISTORIADEUSUARIO_ISSUES.md)

## 1. Estructura del GitHub Project

* **Nombre del Proyecto:** `Directorio Cultural Colombia - Sprint 1`
* **Visibilidad recomendada:** `Public` (para que el instructor pueda inspeccionarlo sin restricción de permisos).
* **Campo de estado (`Status`):**
  1. `Backlog` (Trabajo identificado para iteraciones futuras)
  2. `Ready` (Trabajo priorizado y listo para comenzar)
  3. `In Progress` (Trabajo en ejecución)
  4. `In Review` (Trabajo con Pull Request abierto pendiente de revisión)
  5. `Done` (Trabajo terminado y verificado con la DoD)
* **Campo personalizado (`Priority` - Single Select):** `High`, `Medium`, `Low`

---

## 2. Distribución Completa en el Tablero (8 Historias de Usuario / Issues)

| ID / Issue | Título | Priority | Responsable | Rama asociada | Estado (`Status`) |
|---|---|---|---|---|---|
| **HU-01** ([#1](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/1)) | Consulta inicial de espacios culturales reales y atribución oficial de `datos.gov.co` | `High` | `Andres` | `feature/cultural-spaces-listing` | `Done` |
| **HU-02** ([#2](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/2)) | Búsqueda por palabra clave y filtrado combinado por departamento, municipio y tipo | `High` | `Santiago` | `feature/search-and-filter` + `PR #4` | `In Review` |
| **HU-03** ([#3](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/3)) | Resumen estadístico rápido de la oferta cultural en la consulta actual | `Medium` | `Juliana` | `feature/results-summary` | `Done` |
| **HU-04** | Saneamiento de entradas contra inyección SoQL (`$where`) y manejo de búsquedas en blanco | `High` | `Santiago` | `feature/search-and-filter` | `Done` |
| **HU-05** | Normalización de registros con datos incompletos y retroalimentación en búsquedas sin coincidencias | `High` | `Juliana` | `feature/improve-empty-states` (`PR #4`) | `In Review` |
| **HU-06** | Contingencia automática con respaldo CSV local ante caídas o timeouts de la API Socrata | `Medium` | `Andres` | `feature/cultural-spaces-listing` | `Done` |
| **HU-07** | Paginación de resultados (`$offset` y `$limit`) para explorar más de 40 espacios por consulta | `Medium` | `Andres` | Backlog Sprint 2 | `Ready` |
| **HU-08** | Autocompletado dinámico de municipios según el departamento seleccionado | `Low` | `Juliana` | Backlog Sprint 2 | `Backlog` |
