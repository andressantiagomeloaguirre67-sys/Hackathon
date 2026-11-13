# Configuración del GitHub Project y Matriz Arquitectónica de 15 Historias de Usuario

* **Repositorio:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon
* **URL de Projects del repositorio:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/projects
* **Catálogo Arquitectónico de las 15 Historias de Usuario (listo para copiar):** [`docs/HISTORIADEUSUARIO_ISSUES.md`](../HISTORIADEUSUARIO_ISSUES.md)

## 1. Estructura del GitHub Project

* **Nombre del Proyecto:** `Directorio Cultural Colombia - Sprint 1`
* **Visibilidad:** `Public`
* **Columnas (`Status`):** `Backlog`, `Ready`, `In Progress`, `In Review`, `Done`
* **Campo personalizado (`Priority`):** `High`, `Medium`, `Low`

---

## 2. Matriz Completa del Tablero (15 Historias de Usuario en 6 Capas Arquitectónicas)

| ID | Capa Arquitectónica | Título | Priority | Responsable | Estado (`Status`) |
|---|---|---|---|---|---|
| **HU-01** ([#1](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/1)) | 1. Ingesta Socrata | Consulta en tiempo real de espacios culturales desde la API Socrata de `datos.gov.co` | `High` | `Andres` | `Done` |
| **HU-02** ([#2](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/2)) | 3. Búsqueda y Dominio | Búsqueda por palabra clave y filtrado multicriterio por departamento, municipio y tipo | `High` | `Santiago` | `In Review` (`PR #4`) |
| **HU-03** ([#3](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/3)) | 3. Analítica en Memoria | Resumen estadístico dinámico de la oferta cultural en la consulta actual | `Medium` | `Juliana` | `Done` |
| **HU-04** | 2. Seguridad SoQL | Saneamiento de entradas contra inyección SoQL (`$where`) y acotamiento de `$limit` | `High` | `Santiago` | `Done` |
| **HU-05** | 2. Limpieza de Datos | Normalización de registros con datos ausentes o comodines (`"Sin Dato"`, `"No registra"`) | `High` | `Juliana` | `In Review` (`PR #4`) |
| **HU-06** | 1. Resiliencia / Fallback | Conmutación automática (Fallback) a CSV local real ante fallos o timeouts de red | `High` | `Andres` | `Done` |
| **HU-09** | 1. Gobernanza de Datos | Trazabilidad de fuente activa (API en vivo vs CSV local) y atribución oficial MinCultura | `Medium` | `Andres` | `Done` |
| **HU-10** | 4. Estados de Interfaz | Gestión diferenciada de búsqueda en blanco, estado vacío con detalle de filtros y restablecimiento | `High` | `Santiago` | `Done` |
| **HU-11** | 4. UI/UX y Accesibilidad | Interfaz responsiva (CSS Grid) con semántica HTML5 y atributos de accesibilidad ARIA | `Medium` | `Juliana` | `Done` |
| **HU-12** | 5. QA y Testing | Suite de pruebas automatizadas desacopladas con Mocks HTTP para casos críticos y bordes | `High` | `Juliana` | `Done` |
| **HU-13** | 5. Arquitectura y Seguridad | Configuración Django sin estado (Stateless), protección de `SECRET_KEY` por entorno y `.gitignore` | `Medium` | `Santiago` | `Done` |
| **HU-07** | 6. Evolución (Sprint 2) | Paginación de resultados (`$offset` y `$limit`) para explorar más de 40 espacios por consulta | `Medium` | `Andres` | `Ready` |
| **HU-14** | 6. Evolución (Sprint 2) | Exportación ciudadana de los resultados filtrados actuales a formato CSV descargable | `Medium` | `Santiago` | `Ready` |
| **HU-08** | 6. Evolución (Sprint 2) | Autocompletado dinámico y tolerancia a tildes en nombres de municipios por departamento | `Low` | `Juliana` | `Backlog` |
| **HU-15** | 6. Evolución (Sprint 2) | Integración de coordenadas geográficas (`latitud`/`longitud`) con enlace directo a mapa externo | `Low` | `Andres` | `Backlog` |
