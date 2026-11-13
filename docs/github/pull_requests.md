# Pull Requests del Sprint (Listos para copiar en GitHub)

> **Nota de transparencia:** Al no contar con `gh` CLI ni un repositorio remoto configurado en este entorno local, las ramas se fusionaron a `main` mediante commits de merge explícitos (`--no-ff`) tras su revisión y verificación. Aquí se documentan los textos íntegros de los Pull Requests en español listos para copiar en GitHub.

---

## Pull Request #1: Listado inicial de espacios culturales reales y respaldo CSV local

* **Rama origen:** `feature/cultural-spaces-listing` → **Rama destino:** `main`
* **Estado:** `Merged`
* **Referencia:** `Refs #1`

### Resumen
Implementa la capa de servicio (`cultural_spaces/services.py`), las rutas (`cultural_spaces/urls.py`), la vista principal (`cultural_spaces/views.py`) y la plantilla HTML (`cultural_spaces/templates/cultural_spaces/index.html`) para consultar y presentar los registros reales del dataset **Espacios de las Artes, las Culturas y los Saberes (`te39-v28f`)** desde `datos.gov.co`. Incluye normalización de registros incompletos y un respaldo local en `/data/cultural_spaces_sample.csv` descargado del mismo dataset oficial.

### Por qué se realizó
Los ciudadanos necesitan una vista inicial clara y confiable de los espacios culturales del país que no se rompa cuando existan campos vacíos o valores `"Sin Dato"` en la fuente original, y que mantenga disponibilidad si ocurre una caída temporal en la API Socrata.

### Cómo se verificó
1. Se ejecutó `python manage.py check` sin errores.
2. Se levantó `python manage.py runserver` y se comprobó la carga de `http://127.0.0.1:8000/` recibiendo `HTTP 200` con 40 tarjetas de espacios culturales reales y atribución visible al Ministerio de las Culturas, las Artes y los Saberes.
3. Se probó mediante pruebas unitarias con mocks (`test_incomplete_record_does_not_break_interface` y `test_api_failure_falls_back_to_local_csv`) que los registros incompletos y los fallos de red se manejan sin errores.

### Revisión de código (Code Review)
- [x] Código, nombres de variables y commits en inglés; interfaz en español.
- [x] Sin modelos ni base de datos (`DATABASES = {}`).
- [x] Timeout configurado (`DEFAULT_TIMEOUT = 8`) en `requests.get`.
- [x] Atribución de fuente oficial visible en encabezado y pie de página.

`Refs #1`

---

## Pull Request #2: Búsqueda y filtrado seguro con saneamiento SoQL (`$where`)

* **Rama origen:** `feature/search-and-filter` → **Rama destino:** `main`
* **Estado:** `Merged`
* **Referencia:** `Refs #2`

### Resumen
Añade el formulario de búsqueda por nombre (`q`) y filtrado por municipio (`municipio`), departamento (`departamento`) y tipo de espacio (`tipo_lugar`). Incorpora las funciones `sanitize_soql_value` y `build_soql_where` en `cultural_spaces/services.py` para escapar comillas simples (`'` → `''`) antes de construir la cláusula `$where` de Socrata, evitando errores de sintaxis o inyección en la consulta. Define también el comportamiento para entradas vacías y búsquedas sin coincidencias.

### Por qué se realizó
Con 29.961 espacios registrados a nivel nacional, es indispensable que el usuario pueda acotar la consulta a su departamento, municipio o categoría de interés de forma segura y recibiendo retroalimentación clara cuando no existan resultados o cuando envíe el formulario en blanco.

### Cómo se verificó
1. Se verificó con `runserver` la búsqueda real `GET /?departamento=Antioquia&tipo_lugar=Biblioteca` (`HTTP 200`, 40 resultados reales).
2. Se verificó la búsqueda sin coincidencias `GET /?q=Inexistente999XYZ` (`HTTP 200`, 0 tarjetas y mensaje claro en español).
3. Se verificó el envío con entrada vacía `GET /?q=+++&municipio=&departamento=&tipo_lugar=` (`HTTP 200`, aviso informativo y listado general).
4. Se verificó el saneamiento de comillas simples `GET /?q=O%27Higgins` (`HTTP 200`, sin error de sintaxis en Socrata) y el test unitario `test_soql_where_sanitizes_single_quotes_and_injection`.

### Revisión de código (Code Review)
- [x] Saneamiento de comillas simples implementado y probado antes de construir `$where`.
- [x] Los filtros también funcionan sobre el archivo CSV de respaldo cuando no hay conexión.
- [x] Mensajes claros en español para búsqueda vacía y sin resultados.

`Refs #2`

---

## Pull Request #3: Resumen estadístico de resultados y suite de pruebas automatizadas

* **Rama origen:** `feature/results-summary` → **Rama destino:** `main`
* **Estado:** `Merged`
* **Referencia:** `Refs #3`

### Resumen
Agrega la función `summarize_spaces` en `cultural_spaces/services.py` y la barra de tarjetas de resumen en `index.html` (total de espacios mostrados, municipios en la consulta, departamentos representados y categorías principales). Incorpora además la suite completa de pruebas en `cultural_spaces/tests.py` usando `unittest.mock.patch` para los 4 casos obligatorios y casos de seguridad/resiliencia.

### Por qué se realizó
Permite al ciudadano o investigador dimensionar rápidamente la distribución de espacios culturales en la consulta actual y garantiza mediante pruebas automatizadas repetibles (sin depender de red durante los tests) que los 4 escenarios obligatorios funcionan correctamente.

### Cómo se verificó
1. Se ejecutó `.venv/bin/python manage.py test -v 2`, pasando los 6 tests en `0.021s` (`OK`).
2. Se verificó manualmente en el servidor local que las tarjetas de resumen muestran conteos reales en búsquedas normales y `0` cuando no hay coincidencias.

### Revisión de código (Code Review)
- [x] Los 4 casos obligatorios están cubiertos con mocks HTTP en `cultural_spaces/tests.py`.
- [x] El resumen maneja listas vacías sin errores.
- [x] Integrado limpiamente en `main`.

`Refs #3`
