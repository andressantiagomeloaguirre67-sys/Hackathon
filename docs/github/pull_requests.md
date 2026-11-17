# Pull Requests revisados e integrados

Listado: https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pulls?q=is%3Apr+is%3Aclosed

Cada Pull Request fue revisado por un integrante distinto a su autor, que ejecutó las pruebas en su equipo, lo probó en el navegador, lo aprobó con un comentario y lo fusionó en `main`.

| PR | Título | Autor | Revisó y fusionó | Historias | Pruebas al fusionar |
|---|---|---|---|---|---|
| [#4](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4) | Mejorar manejo de respuestas vacías, placeholders extendidos y límite seguro en consultas Socrata | Andres | Juliana | HU-02, HU-04, HU-05, HU-10 (`Refs #2`) | 7 OK |
| [#17](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/17) | Calcular indicadores sobre todos los resultados, mostrar el total real y agregar una muestra de respaldo representativa | Juliana | Andres | HU-03, HU-06, HU-09, HU-12 (`Refs #3`, `Refs #1`) | 13 OK |
| [#18](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/18) | Paginar resultados con `$offset` conservando los filtros | Andres | Juliana | HU-07 (`Refs #8`) | 19 OK |
| [#19](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/19) | Descarga CSV de resultados y autocompletado de municipios sin tildes | Juliana | Andres | HU-14, HU-08 (`Refs #10`, `Refs #9`) | 33 OK |

## Hallazgos de las revisiones
* **PR #4:** la revisión detectó que la verificación `assertContains(response, "TerminoInexistenteXYZ999")` también pasaba sin el cambio de la plantilla, porque el término ya aparecía en la casilla de búsqueda. Se corrigió en el PR #17 verificando el texto propio del bloque ("Filtros aplicados sin coincidencias").
* **PR #19:** la HU-14 se implementó con una función de exportación propia en lugar de reutilizar `fetch_cultural_spaces`, que devuelve 40 registros por página; la decisión quedó explicada en la descripción del PR.

## Nota
Los commits "Merge pull request #1/#2/#3" del inicio del historial son fusiones locales de las primeras ramas, no Pull Requests de GitHub.
