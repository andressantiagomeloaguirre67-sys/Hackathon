# Directorio Ciudadano de Espacios de las Artes, las Culturas y los Saberes (Colombia)

Aplicación web construida en **Python + Django** (sin modelos ni base de datos propia) que consume en tiempo real datos abiertos oficiales del portal [datos.gov.co](https://www.datos.gov.co/) para permitir a ciudadanos, estudiantes y gestores culturales buscar, filtrar y resumir escenarios culturales, bibliotecas, museos, casas de cultura, escuelas de música, archivos históricos y sitios patrimoniales en toda Colombia.

---

## 1. Fuente de Datos Oficial

* **Nombre del conjunto de datos:** Espacios de las Artes, las Culturas y los Saberes
* **Identificador Socrata:** `te39-v28f`
* **Entidad publicadora:** Ministerio de las Culturas, las Artes y los Saberes (MinCultura) — Bogotá D.C.
* **URL en el portal de Datos Abiertos:** https://www.datos.gov.co/Cultura/Espacios-de-las-Artes-las-Culturas-y-los-Saberes/te39-v28f
* **Endpoint API Socrata (JSON):** `https://www.datos.gov.co/resource/te39-v28f.json`
* **Respaldo local real (contingencia sin conexión):** `/data/cultural_spaces_sample.csv` (muestra real descargada directamente del endpoint oficial `te39-v28f.csv`).

---

## 2. Instalación y Ejecución Paso a Paso

### Requisitos previos
* Python 3.10+ (verificado en **Python 3.14.8**)
* Git

### Pasos de instalación

1. **Clonar o ubicarse en la carpeta del repositorio:**
   ```bash
   cd /home/andres/Proyectos/Hackaton
   ```

2. **Crear y activar el entorno virtual (`venv`):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar las dependencias con versiones fijadas:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la suite de pruebas automatizadas (`test`):**
   ```bash
   python manage.py test -v 2
   ```

5. **Iniciar el servidor de desarrollo (`runserver`):**
   ```bash
   python manage.py runserver
   ```
   Luego abre en el navegador: **http://127.0.0.1:8000/**

---

## 3. Estructura del Proyecto

```text
.
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Configuración Django sin base de datos ni secretos en el repo
│   ├── urls.py              # Enrutador raíz
│   └── wsgi.py
├── cultural_spaces/
│   ├── __init__.py
│   ├── apps.py
│   ├── services.py          # Cliente Socrata API, saneamiento SoQL ($where), normalización y fallback CSV
│   ├── templates/
│   │   └── cultural_spaces/
│   │       └── index.html   # Interfaz en español con formulario, resumen, tarjetas y atribución
│   ├── tests.py             # Pruebas automatizadas con mocks HTTP para los casos obligatorios
│   ├── urls.py              # Rutas de la aplicación
│   └── views.py             # Vista principal de búsqueda, filtrado y resumen
├── data/
│   └── cultural_spaces_sample.csv # Datos reales del mismo dataset para contingencia offline
├── docs/
│   └── github/
│       ├── issues.md        # Issues del Product Backlog (#1, #2, #3)
│       ├── project.md       # Configuración y estado real del GitHub Project
│       └── pull_requests.md # Registro de Pull Requests revisados e integrados
├── manage.py
├── requirements.txt         # Versiones fijadas (Django==6.1.3, requests==2.34.2, etc.)
└── README.md
```

---

## 4. Descubrimiento

* **Problema (hipótesis, no hecho confirmado):** Se plantea como **hipótesis** que ciudadanos, estudiantes, turistas y gestores culturales en Colombia tienen dificultades para encontrar en un solo lugar qué espacios culturales, bibliotecas, museos o escenarios artísticos existen en su municipio o departamento, dado que la información proviene de múltiples registros técnicos sectoriales (PULEP, Red Nacional de Bibliotecas Públicas, SIMCO, SIlep, ICANH).
* **Usuario objetivo:** Ciudadanos, estudiantes, docentes, investigadores, turistas y gestores culturales en Colombia.
* **Fuente:** [Espacios de las Artes, las Culturas y los Saberes (`te39-v28f`)](https://www.datos.gov.co/resource/te39-v28f.json) — **Ministerio de las Culturas, las Artes y los Saberes (MinCultura)**, con **29.961 registros** verificados y última actualización del `2026-11-13`.
* **Campos usados:** `nombre_del_lugar`, `tipo_lugar`, `departamento`, `municipio`, `direcci_n_f_sica`, `descripci_n`, `fuente` y `divipola`.
* **Funcionalidad principal:** **Buscar, filtrar y resumir** espacios culturales por palabra clave en el nombre, municipio, departamento y tipo de lugar.
* **Limitaciones:**
  * El dataset no cuenta con columnas de teléfono, correo electrónico ni horarios de atención.
  * Las direcciones físicas no siguen un estándar único y algunos registros patrimoniales o arqueológicos carecen de dirección urbana detallada.

---

## 5. Planificación Ágil

### Product Goal
Permitir que cualquier ciudadano o gestor cultural en Colombia descubra de forma rápida, confiable y accesible los espacios culturales, bibliotecas, museos y escenarios artísticos de su municipio o departamento utilizando datos abiertos oficiales del Ministerio de las Culturas, las Artes y los Saberes.

### Product Backlog (3 PBIs)

#### PBI #1 — Consulta de espacios culturales reales y manejo resiliente de datos (Prioridad: High)
* **Historia de usuario:** *Como* ciudadano interesado en la oferta cultural de mi territorio, *quiero* visualizar un listado claro de espacios culturales reales obtenidos de `datos.gov.co` junto con su fuente oficial, *para* conocer qué lugares culturales existen y dónde están ubicados incluso si algún registro tiene campos incompletos.
* **Criterios de aceptación comprobables:**
  1. Consulta `https://www.datos.gov.co/resource/te39-v28f.json` con `timeout=8` segundos y muestra nombre, tipo de lugar, municipio, departamento, dirección física, descripción y fuente.
  2. Si un registro carece de `direcci_n_f_sica`, `descripci_n` u otro campo, muestra valores por defecto legibles (`"No especificada"`, `"Sin descripción disponible"`) sin romper la interfaz.
  3. Si falla la conexión con Socrata API, usa automáticamente `/data/cultural_spaces_sample.csv` e informa del respaldo en pantalla.
  4. Muestra atribución explícita al Ministerio de las Culturas, las Artes y los Saberes y enlace a `datos.gov.co`.

#### PBI #2 — Búsqueda y filtrado seguro por municipio, departamento, tipo de espacio y nombre (Prioridad: High)
* **Historia de usuario:** *Como* estudiante o gestor cultural, *quiero* buscar espacios por palabra clave y filtrar por departamento, municipio o tipo de espacio cultural, *para* encontrar rápidamente los lugares específicos que me interesan en mi localidad sin tener que revisar miles de registros.
* **Criterios de aceptación comprobables:**
  1. Formulario HTML con campos `q` (nombre), `municipio`, `departamento` y `tipo_lugar` que construyen la cláusula `$where` en Socrata.
  2. Saneamiento de entrada (`sanitize_soql_value`) que escapa comillas simples (`'` → `''`), limpia caracteres de control y limita longitud antes de armar `$where`.
  3. **Entrada vacía:** Al enviar el formulario vacío o con espacios en blanco, presenta el listado general e informa que no se ingresaron filtros.
  4. **Sin coincidencias:** Cuando la consulta retorna 0 registros, muestra un mensaje claro en español y botón para limpiar filtros.

#### PBI #3 — Resumen estadístico rápido de los resultados consultados (Prioridad: Medium)
* **Historia de usuario:** *Como* ciudadano o investigador cultural, *quiero* ver indicadores resumidos sobre los resultados de mi consulta (total de espacios mostrados, número de municipios representados y tipos de espacios predominantes), *para* dimensionar de un vistazo la diversidad cultural del territorio filtrado.
* **Criterios de aceptación comprobables:**
  1. Panel superior con tarjetas de resumen: total de espacios mostrados, municipios en la consulta, departamentos representados y conteo de las 4 categorías principales.
  2. Con 0 resultados, los indicadores muestran `0` y `"Sin categorías para mostrar"` sin errores.

### Sprint Goal
Entregar un recorrido web completo y verificado en Django que permita buscar, filtrar de forma segura y resumir espacios culturales reales de Colombia desde la API de `datos.gov.co`, manejando entradas vacías, búsquedas sin resultados, registros incompletos y contingencias de red.

### Sprint Backlog
* **Objetivo:** Completar e integrar en `main` los PBIs #1, #2 y #3 con pruebas unitarias y manuales verificadas.
* **Ramas ejecutadas e integradas:**
  * `feature/cultural-spaces-listing` → `main` (PR #1, `Refs #1`)
  * `feature/search-and-filter` → `main` (PR #2, `Refs #2`)
  * `feature/results-summary` → `main` (PR #3, `Refs #3`)

---

## 6. Definición de Hecho (DoD) — Estado Real

- [x] **Django inicia sin errores:** Verificado con `.venv/bin/python manage.py check` (`System check identified no issues (0 silenced)`).
- [x] **El recorrido se completa en el navegador:** Verificado levantando `python manage.py runserver` y ejecutando consultas reales de inicio, filtrado por departamento/tipo, entrada vacía, cero coincidencias y comillas simples.
- [x] **Datos reales con fuente identificada:** Consume en vivo `https://www.datos.gov.co/resource/te39-v28f.json` (MinCultura) y muestra atribución en encabezado y pie de página.
- [x] **Criterios de aceptación cumplidos:** Los 3 PBIs cumplen todos sus criterios de aceptación.
- [x] **Entradas inválidas o resultados vacíos no rompen la app:** Comprobado con entradas en blanco, comillas simples (`O'Higgins' OR '1'='1`), búsquedas sin coincidencias y registros con valores `None` / `"Sin Dato"`.
- [x] **Se ejecutó una prueba real:** Ejecutados los 6 tests automatizados (`python manage.py test -v 2`) y la prueba manual contra el servidor en ejecución.
- [x] **Cambios revisados e integrados en `main`:** Ramas por PBI fusionadas a `main` mediante commits de merge (`--no-ff`) con referencia `Refs #N`.
- [x] **`README.md` permite instalar y ejecutar:** Incluye instrucciones paso a paso verificadas.
- [x] **Issues y Project reflejan el estado real:** Documentados y actualizados a `Done` en `/docs/github/project.md`, `/docs/github/issues.md` y `/docs/github/pull_requests.md` (nota de transparencia: `gh` CLI no está instalado en el entorno local, por lo que no se crearon en un servidor remoto de GitHub sino que quedaron listos en `/docs/github/`).

---

## 7. Resultado Real de las Pruebas

### 7.1 Pruebas Automatizadas (`python manage.py test -v 2`)
Comando ejecutado:
```bash
.venv/bin/python manage.py test -v 2
```
Salida real obtenida:
```text
Found 6 test(s).
Skipping setup of unused database(s): default.
System check identified no issues (0 silenced).
test_api_failure_falls_back_to_local_csv (cultural_spaces.tests.CulturalSpacesTests.test_api_failure_falls_back_to_local_csv)
Verify network errors fall back gracefully to /data/cultural_spaces_sample.csv. ... ok
test_empty_input_submission_has_defined_behavior (cultural_spaces.tests.CulturalSpacesTests.test_empty_input_submission_has_defined_behavior)
Case 3 (Empty input): submitting blank/whitespace filters shows general results and notice. ... ok
test_incomplete_record_does_not_break_interface (cultural_spaces.tests.CulturalSpacesTests.test_incomplete_record_does_not_break_interface)
Case 4 (Incomplete data): missing, None, or 'Sin Dato' fields use safe defaults without crashing. ... ok
test_no_matches_renders_clear_empty_message (cultural_spaces.tests.CulturalSpacesTests.test_no_matches_renders_clear_empty_message)
Case 2 (No matches): displays a clear Spanish message when search returns zero records. ... ok
test_normal_search_renders_matching_spaces_and_summary (cultural_spaces.tests.CulturalSpacesTests.test_normal_search_renders_matching_spaces_and_summary)
Case 1 (Normal search): returns matching spaces, summary indicators, and source attribution. ... ok
test_soql_where_sanitizes_single_quotes_and_injection (cultural_spaces.tests.CulturalSpacesTests.test_soql_where_sanitizes_single_quotes_and_injection)
Verify user input single quotes are escaped before building $where. ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.021s

OK
```

### 7.2 Prueba Manual con `python manage.py runserver` y Datos Reales en Vivo
Se inició el servidor local en `127.0.0.1:8000` y se verificaron los casos contra `datos.gov.co`:
```text
Home / Initial list: HTTP 200 | Cards rendered: 40 | Attribution present: True
Normal filter (Antioquia + Biblioteca): HTTP 200 | Cards rendered: 40 | Attribution present: True
Empty input submission: HTTP 200 | Cards rendered: 40 | Attribution present: True
Zero matches: HTTP 200 | Cards rendered: 0 | Attribution present: True
Single quote sanitization: HTTP 200 | Cards rendered: 0 | Attribution present: True
[13/Nov/2026 14:02:06] "GET / HTTP/1.1" 200 45556
[13/Nov/2026 14:02:12] "GET /?departamento=Antioquia&tipo_lugar=Biblioteca HTTP/1.1" 200 38844
[13/Nov/2026 14:02:20] "GET /?q=+++&municipio=&departamento=&tipo_lugar= HTTP/1.1" 200 40178
[13/Nov/2026 14:02:23] "GET /?q=Inexistente999XYZ HTTP/1.1" 200 15839
[13/Nov/2026 14:02:23] "GET /?q=O%27Higgins HTTP/1.1" 200 15836
```

---

## 8. Retrospectiva del Sprint

* **Qué funcionó bien:**
  * La separación estricta entre la vista (`views.py`) y la capa de servicios (`services.py`) permitió implementar el saneamiento SoQL (`$where`), la normalización de registros incompletos y el respaldo CSV local en un solo punto fácil de probar con `SimpleTestCase` sin requerir base de datos.
  * Validar primero los metadatos y las muestras reales de `datos.gov.co` en el Paso 1 garantizó elegir un dataset actualizado (`te39-v28f`) con columnas limpias para filtrar (`departamento`, `municipio`, `tipo_lugar`, `nombre_del_lugar`).
* **Qué obstáculo hubo:**
  * En el entorno de desarrollo no estaba instalada la herramienta `gh` CLI ni existía un repositorio remoto configurado en GitHub, además de diferencias de capitalización y tildes en los nombres de municipios dentro de Socrata.
* **Acción concreta de mejora para el siguiente Sprint:**
  * Incorporar paginación (`$offset` y `$limit`) en la interfaz y autocompletado dinámico de municipios por departamento consultando una agregación ligera (`$select=municipio&$group=municipio`) con caché en memoria para evitar errores de escritura con tildes.
