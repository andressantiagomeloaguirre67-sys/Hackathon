# Issues: historias de usuario y estado

La fuente oficial y actualizada de cada historia (descripción, criterios de aceptación y estado) son los **issues de GitHub**:
https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues?q=is%3Aissue

El texto original de planificación de las 15 historias está en [`../HISTORIADEUSUARIO_ISSUES.md`](../HISTORIADEUSUARIO_ISSUES.md). Algunos criterios se actualizaron en GitHub al implementarlos (por ejemplo, HU-03, HU-06, HU-07, HU-08, HU-09, HU-12 y HU-14).

GitHub numera issues y Pull Requests con la misma secuencia, por eso el número del issue no coincide con el de la historia (por ejemplo, HU-07 es el issue #8).

| Historia | Issue | Título | Prioridad (P0 alta, P1 media, P2 baja) | Responsable | Estado | Integrada en |
|---|---|---|---|---|---|---|
| HU-01 | [#1](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/1) | Consulta en tiempo real desde la API Socrata | P0 | Andres | Done | Código base |
| HU-02 | [#2](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/2) | Búsqueda por palabra clave y filtros | P0 | Santiago | Done | Código base y PR #4 |
| HU-03 | [#3](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/3) | Resumen estadístico sobre todos los resultados | P1 | Juliana | Done | PR #17 |
| HU-04 | [#5](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/5) | Saneamiento SoQL y acotamiento de `$limit` | P0 | Santiago | Done | Código base y PR #4 |
| HU-05 | [#6](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/6) | Normalización de datos ausentes o comodines | P0 | Juliana | Done | Código base y PR #4 |
| HU-06 | [#7](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/7) | Respaldo automático con CSV local | P0 | Andres | Done | Código base y PR #17 |
| HU-07 | [#8](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/8) | Paginación con `$offset` | P1 | Andres | Done | PR #18 |
| HU-08 | [#9](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/9) | Autocompletado de municipios y tolerancia a tildes | P2 | Juliana | Done | PR #19 |
| HU-09 | [#12](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/12) | Fuente activa y atribución oficial | P1 | Andres | Done | Código base y PR #17 |
| HU-10 | [#13](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/13) | Búsqueda en blanco, estado vacío y restablecimiento | P0 | Santiago | Done | Código base y PR #4 |
| HU-11 | [#14](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/14) | Interfaz responsiva y accesible | P1 | Juliana | Done | Código base |
| HU-12 | [#15](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/15) | Pruebas automatizadas con mocks HTTP (33) | P0 | Juliana | Done | Todos los PRs |
| HU-13 | [#16](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/16) | Configuración sin estado, `SECRET_KEY` por entorno y `.gitignore` | P1 | Santiago | Done | Código base |
| HU-14 | [#10](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/10) | Descarga CSV de los resultados filtrados | P1 | Juliana (reasignada) | Done | PR #19 |
| HU-15 | [#11](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/11) | Enlace a mapa con coordenadas | P2 | Andres | Backlog | Siguiente ciclo |

**Nota sobre responsables:** la columna muestra la asignación de la planificación. El código base inicial fue escrito por Andres; los cambios posteriores están en los Pull Requests, cada uno con su autor y su revisor (ver [`pull_requests.md`](pull_requests.md)).
