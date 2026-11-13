# Directorio Ciudadano de Espacios de las Artes, las Culturas y los Saberes (Colombia)

Aplicación web construida en **Python + Django** (sin modelos ni base de datos propia) que consume en tiempo real datos abiertos oficiales del portal [datos.gov.co](https://www.datos.gov.co/) para permitir a ciudadanos, estudiantes y gestores culturales buscar, filtrar y resumir escenarios culturales, bibliotecas, museos, casas de cultura, escuelas de música, archivos históricos y sitios patrimoniales en toda Colombia.

---

## Enlaces Reales en GitHub

* **Repositorio remoto:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon
* **Rama principal (`main`):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/tree/main
* **Pull Request #4 (abierto, con `Refs #2`, pendiente de revisión y fusión):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4
* **Issues creados en GitHub:**
  * **Issue #1 (PBI #1 - High):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/1
  * **Issue #2 (PBI #2 - High):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/2
  * **Issue #3 (PBI #3 - Medium):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/3
* **GitHub Project del repositorio:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/projects (estructura documentada en [`docs/github/project.md`](docs/github/project.md))

---

## 1. Fuente de Datos Oficial (Verificada en `/api/views/te39-v28f.json`)

Datos verificados directamente desde https://www.datos.gov.co/api/views/te39-v28f.json:

* **Nombre del conjunto de datos (`name`):** `Espacios de las Artes, las Culturas y los Saberes`
* **Identificador Socrata (`id`):** `te39-v28f`
* **Entidad publicadora (`attribution`):** `Ministerio de las Culturas, las Artes y los Saberes - MinCultura, Bogotá D.C.`
* **Autor de la tabla (`tableAuthor.displayName`):** `Ministerio de las Culturas, las Artes y los Saberes - Oficina de Planeacion`
* **Fecha de última actualización de filas (`rowsUpdatedAt`):** `1794547256` → **`2026-11-13 05:20:56 UTC`** (`viewLastModified`: `1794547225` → `2026-11-13 05:20:25 UTC`)
* **Fecha de publicación (`publicationDate`):** `1778790821` → `2026-05-14 20:33:41 UTC`
* **URL en el portal de Datos Abiertos:** https://www.datos.gov.co/Cultura/Espacios-de-las-Artes-las-Culturas-y-los-Saberes/te39-v28f
* **Endpoint API Socrata (JSON):** `https://www.datos.gov.co/resource/te39-v28f.json`
* **Respaldo local real (contingencia sin conexión):** `/data/cultural_spaces_sample.csv` (muestra real descargada del endpoint `te39-v28f.csv`).

---

## 2. Instalación y Ejecución Paso a Paso

### Requisitos previos
* Python 3.10+ (verificado en **Python 3.14.8**)
* Git

### Pasos de instalación

1. **Clonar el repositorio y entrar al directorio:**
   ```bash
   git clone https://github.com/andressantiagomeloaguirre67-sys/Hackathon.git
   cd Hackathon
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

4. **Verificar la configuración de Django (`check`):**
   ```bash
   python manage.py check
   ```

5. **Ejecutar la suite de pruebas automatizadas (`test`):**
   ```bash
   python manage.py test -v 2
   ```

6. **Iniciar el servidor de desarrollo (`runserver`):**
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
│   ├── settings.py          # Configuración Django sin base de datos ni secretos reales en el repo
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
│       └── pull_requests.md # Descripción del Pull Request abierto (pendiente de revisión)
├── manage.py
├── requirements.txt         # Versiones fijadas (Django==6.1.3, requests==2.34.2, etc.)
└── README.md
```

---

## 4. Descubrimiento

* **Problema (hipótesis, no hecho confirmado):** Se plantea como **hipótesis** que ciudadanos, estudiantes, turistas y gestores culturales en Colombia tienen dificultades para encontrar en un solo lugar qué espacios culturales, bibliotecas, museos o escenarios artísticos existen en su municipio o departamento, dado que la información proviene de múltiples registros técnicos sectoriales (PULEP, Red Nacional de Bibliotecas Públicas, SIMCO, SIlep, ICANH).
* **Usuario objetivo:** Ciudadanos, estudiantes, docentes, investigadores, turistas y gestores culturales en Colombia.
* **Fuente:** [Espacios de las Artes, las Culturas y los Saberes (`te39-v28f`)](https://www.datos.gov.co/resource/te39-v28f.json) — **Ministerio de las Culturas, las Artes y los Saberes - MinCultura, Bogotá D.C.** (`rowsUpdatedAt`: `2026-11-13 05:20:56 UTC`, **29.961 registros** verificados con `$select=count(*)`).
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

### Sprint Backlog y Estado en GitHub
* **Ramas subidas en `origin` (`https://github.com/andressantiagomeloaguirre67-sys/Hackathon`):**
  * `main`: Contiene la aplicación base funcional y las pruebas iniciales.
  * `feature/cultural-spaces-listing`: Implementación inicial del PBI #1.
  * `feature/search-and-filter`: Implementación de búsqueda y filtrado SoQL del PBI #2.
  * `feature/results-summary`: Implementación de resumen estadístico y suite de pruebas del PBI #3.
  * `feature/improve-empty-states`: Rama con mejora adicional de manejo de datos incompletos, acotamiento de `$limit` y detalle de filtros en búsquedas vacías (`Refs #2`), **pendiente de revisión y fusión en Pull Request**.

---

## 6. Definición de Hecho (DoD) — Estado Real

- [x] **Django inicia sin errores:** Verificado con `.venv/bin/python manage.py check` (`System check identified no issues (0 silenced)`).
- [x] **El recorrido se completa en el navegador:** Verificado levantando `python manage.py runserver` y ejecutando consultas reales de inicio, filtrado por departamento/tipo, entrada vacía, cero coincidencias y comillas simples.
- [x] **Datos reales con fuente identificada:** Consume en vivo `https://www.datos.gov.co/resource/te39-v28f.json` (`Ministerio de las Culturas, las Artes y los Saberes - MinCultura, Bogotá D.C.`) y muestra atribución en encabezado y pie de página.
- [x] **Criterios de aceptación cumplidos en el código:** Los 3 PBIs cumplen todos sus criterios técnicos y funcionales.
- [x] **Entradas inválidas o resultados vacíos no rompen la app:** Comprobado con entradas en blanco, comillas simples (`O'Higgins' OR '1'='1`), búsquedas sin coincidencias y registros con valores `None` / `"Sin Dato"`.
- [x] **Se ejecutó una prueba real:** Ejecutados los tests automatizados (`python manage.py test -v 2`) y la prueba manual con `runserver`.
- [x] **`README.md` permite instalar y ejecutar:** Incluye instrucciones paso a paso verificadas y enlaces reales a GitHub.
- [x] **Issues (#1, #2, #3) y Pull Request (#4 con `Refs #2`) creados en GitHub:** Verificados en https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues y https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4.
- [ ] **Revisión del Pull Request #4 e integración en `main` (Pendiente):** El PR #4 se encuentra abierto y **pendiente de revisión por un compañero y posterior fusión a `main`**.
- [ ] **Movimiento del Issue #2 a `Done` en el GitHub Project (Pendiente):** Depende de que se revise y fusione el Pull Request #4.

---

## 7. Resultado Real de las Pruebas

### 7.1 Pruebas Automatizadas en `main` (Antes del cambio en `feature/improve-empty-states`)
```text
Found 6 test(s).
Skipping setup of unused database(s): default.
System check identified no issues (0 silenced).
test_api_failure_falls_back_to_local_csv (cultural_spaces.tests.CulturalSpacesTests.test_api_failure_falls_back_to_local_csv) ... ok
test_empty_input_submission_has_defined_behavior (cultural_spaces.tests.CulturalSpacesTests.test_empty_input_submission_has_defined_behavior) ... ok
test_incomplete_record_does_not_break_interface (cultural_spaces.tests.CulturalSpacesTests.test_incomplete_record_does_not_break_interface) ... ok
test_no_matches_renders_clear_empty_message (cultural_spaces.tests.CulturalSpacesTests.test_no_matches_renders_clear_empty_message) ... ok
test_normal_search_renders_matching_spaces_and_summary (cultural_spaces.tests.CulturalSpacesTests.test_normal_search_renders_matching_spaces_and_summary) ... ok
test_soql_where_sanitizes_single_quotes_and_injection (cultural_spaces.tests.CulturalSpacesTests.test_soql_where_sanitizes_single_quotes_and_injection) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.019s

OK
```

### 7.2 Pruebas Automatizadas en `feature/improve-empty-states` (Después del cambio)
```text
Found 7 test(s).
Skipping setup of unused database(s): default.
System check identified no issues (0 silenced).
test_api_failure_falls_back_to_local_csv (cultural_spaces.tests.CulturalSpacesTests.test_api_failure_falls_back_to_local_csv) ... ok
test_empty_input_submission_has_defined_behavior (cultural_spaces.tests.CulturalSpacesTests.test_empty_input_submission_has_defined_behavior) ... ok
test_extended_placeholders_and_invalid_limit_are_handled_safely (cultural_spaces.tests.CulturalSpacesTests.test_extended_placeholders_and_invalid_limit_are_handled_safely) ... ok
test_incomplete_record_does_not_break_interface (cultural_spaces.tests.CulturalSpacesTests.test_incomplete_record_does_not_break_interface) ... ok
test_no_matches_renders_clear_empty_message (cultural_spaces.tests.CulturalSpacesTests.test_no_matches_renders_clear_empty_message) ... ok
test_normal_search_renders_matching_spaces_and_summary (cultural_spaces.tests.CulturalSpacesTests.test_normal_search_renders_matching_spaces_and_summary) ... ok
test_soql_where_sanitizes_single_quotes_and_injection (cultural_spaces.tests.CulturalSpacesTests.test_soql_where_sanitizes_single_quotes_and_injection) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.022s

OK
```

### 7.3 Prueba Manual con `python manage.py runserver` y Datos Reales en Vivo
```text
Home / Initial list: HTTP 200 | Cards rendered: 40 | Attribution present: True
Normal filter (Antioquia + Biblioteca): HTTP 200 | Cards rendered: 40 | Attribution present: True
Empty input submission: HTTP 200 | Cards rendered: 40 | Attribution present: True
Zero matches: HTTP 200 | Cards rendered: 0 | Attribution present: True
Single quote sanitization: HTTP 200 | Cards rendered: 0 | Attribution present: True
```

---

## 8. Retrospectiva del Sprint

* **Qué funcionó bien:**
  * La separación entre `views.py` y `services.py` permitió encapsular el saneamiento de `$where`, la limpieza de datos incompletos y el respaldo CSV local en funciones puras, logrando pruebas unitarias rápidas (`~0.02s`) sin requerir base de datos.
  * El uso de la clave SSH local permitió subir el repositorio y todas las ramas a GitHub sin exponer tokens ni credenciales en ningún archivo del proyecto.
* **Qué obstáculo hubo:**
  * Aunque el acceso SSH a GitHub estaba activo para `git push`, el cliente `gh` CLI no tenía una sesión OAuth iniciada (`gh auth login`), lo que impidió crear automáticamente los Issues, el Project y el Pull Request mediante la API de GitHub sin intervención manual en el navegador.
* **Acción concreta de mejora:**
  * Verificar tanto `ssh -T git@github.com` como `gh auth status` al inicio del Sprint (Paso 1) antes de comenzar la codificación para asegurar que la automatización de tableros e issues esté disponible desde el primer commit.
