# Directorio Ciudadano de Espacios de las Artes, las Culturas y los Saberes (Colombia)

Aplicación web construida en **Python + Django** (sin modelos ni base de datos propia) que consume en tiempo real datos abiertos oficiales del portal [datos.gov.co](https://www.datos.gov.co/) para permitir a ciudadanos, estudiantes y gestores culturales buscar, filtrar y resumir escenarios culturales, bibliotecas, museos, casas de cultura, escuelas de música, archivos históricos y sitios patrimoniales en toda Colombia.

---

## Enlaces Reales en GitHub

* **Repositorio remoto:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon
* **Rama principal (`main`):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/tree/main
* **Historial de Commits en GitHub (`main`):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/commits/main
* **Ramas del repositorio (`branches`):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/branches
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

## 4. Fase 1 — Descubrimiento del Problema

### 4.1 Fuentes candidatas exploradas en `datos.gov.co` y justificación de selección
Durante la exploración en la API de catálogo Socrata (`api.us.socrata.com/api/catalog/v1`) se analizaron metadatos, conteo real y muestras de varias fuentes ciudadanas (descartando las que tenían menos de 200 registros o más de 3 años sin actualizar, como `rpqd-dc8v`, `ideb-ck93`, `g8hy-gwg8` y `2h8t-2zik`) y se compararon 3 candidatos viables:

1. `b4dp-ximh` — *Prestadores de Salud Departamento de Antioquia* (Gobernación de Antioquia, 17.232 registros, actualizado `2025-03-19`).
2. **`te39-v28f` — *Espacios de las Artes, las Culturas y los Saberes* (Ministerio de las Culturas, las Artes y los Saberes, 29.961 registros, actualizado `2026-11-13`) — [SELECCIONADO]**.
3. `7tec-5fhs` — *Listado de Instituciones Educativas Oficiales y No Oficiales del Departamento del Atlántico* (Gobernación del Atlántico, 212 registros, actualizado `2024-08-21`).

* **Justificación de selección (`te39-v28f`):** Tiene cobertura nacional (todos los departamentos y municipios de Colombia), fue actualizado el `2026-11-13`, cuenta con 29.961 registros reales y posee columnas categóricas y geográficas claras (`departamento`, `municipio`, `tipo_lugar`, `nombre_del_lugar`) ideales para un recorrido completo de búsqueda, filtrado y resumen ciudadano.

### 4.2 Entregable del Descubrimiento
* **Nombre provisional de la aplicación:** *Directorio Ciudadano de Espacios de las Artes, las Culturas y los Saberes de Colombia*.
* **Problema o hipótesis de necesidad (hipótesis, no hecho comprobado):** Se formula como **hipótesis** (al no haber sido contrastada aún con usuarios reales en campo) que ciudadanos, estudiantes, turistas y gestores culturales tienen dificultades para localizar en un único punto qué escenarios culturales, bibliotecas, museos o casas de cultura existen en su municipio o departamento, dado que los registros oficiales provienen de sistemas sectoriales separados (PULEP, Red Nacional de Bibliotecas Públicas, SIMCO, SIlep, ICANH).
* **Usuario o beneficiario potencial y decisión/acción que le facilita:** Ciudadanos, estudiantes, docentes, investigadores, turistas y gestores culturales en Colombia. La aplicación les facilita **identificar y decidir a qué espacios culturales acudir o con cuáles articular actividades culturales en su municipio o departamento**.
* **Fuente:** [Espacios de las Artes, las Culturas y los Saberes (`te39-v28f`)](https://www.datos.gov.co/resource/te39-v28f.json) — **Ministerio de las Culturas, las Artes y los Saberes - MinCultura, Bogotá D.C.** (`rowsUpdatedAt`: `2026-11-13 05:20:56 UTC`, **29.961 registros** verificados con `$select=count(*)`).
* **Campos o variables relevantes y alcance de la información:** `nombre_del_lugar` (nombre oficial), `tipo_lugar` (categoría del espacio), `departamento`, `municipio`, `direcci_n_f_sica`, `descripci_n`, `fuente` (sistema origen) y `divipola`. Alcance: nacional (32 departamentos y Bogotá D.C.).
* **Funcionalidad principal y valor esperado:** **Buscar, filtrar y resumir** espacios culturales por palabra clave en el nombre, municipio, departamento y tipo de lugar, ofreciendo indicadores resumidos de cuántos espacios y categorías existen en el territorio consultado.
* **Limitaciones conocidas y riesgos de implementación:**
  * *Limitaciones de los datos:* No incluye teléfono, correo electrónico ni horarios de atención; las direcciones físicas no están estandarizadas y algunos registros arqueológicos carecen de dirección urbana detallada.
  * *Riesgos de implementación y mitigación:* Posible latencia o caída temporal de la API Socrata (mitigado con `timeout=8` segundos y archivo de respaldo real `/data/cultural_spaces_sample.csv`) y posibles errores de sintaxis SoQL por caracteres especiales en la entrada del usuario (mitigado con saneamiento de comillas simples en `sanitize_soql_value`).

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

### Sprint Backlog, Ramas y Commits en GitHub
* **Ramas y commits principales subidos en `origin` ([ver historial de commits](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/commits/main)):**
  * `8488d4a` (`main`): `docs: add discovery, agile planning, and DoD to README`
  * `d183d76` (`main`): `docs: add GitHub Project board and backlog issues in docs/github`
  * `3f321c9` (`main`): `chore: initialize stateless Django project and pinned requirements`
  * `f0146f8` (`feature/cultural-spaces-listing`): `feat: add Socrata API client, CSV fallback, and cultural spaces listing (Refs #1)`
  * `4e0cf39` (`feature/search-and-filter`): `feat: add sanitized SoQL search and filter form with empty and zero-result handling (Refs #2)`
  * `8afd103` (`feature/results-summary`): `feat: add statistical summary bar for cultural spaces results (Refs #3)`
  * `fe2f2c7` (`feature/results-summary`): `test: add mocked unit and integration tests for mandatory scenarios (Refs #1, #2, #3)`
  * `83da456` (`feature/improve-empty-states`): `feat: clamp Socrata query limit, handle extended placeholders, and show active filters on empty results (Refs #2)` — **Abierto en [Pull Request #4](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4), pendiente de revisión y fusión**.

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

## 8. Fase 4 — Revisión del Sprint (Sprint Review) y Retrospectiva

### 8.1 Revisión del Sprint (Sprint Review)
* **Problema o hipótesis identificada y para quién:** Hipótesis de dispersión de la oferta de infraestructura cultural pública y privada en Colombia para ciudadanos, estudiantes, investigadores y gestores culturales.
* **Fuente de datos utilizada y limitaciones observadas:** Dataset oficial `te39-v28f` (*Espacios de las Artes, las Culturas y los Saberes*) del Ministerio de las Culturas, las Artes y los Saberes en `datos.gov.co` (29.961 registros). Limitaciones: ausencia de teléfonos/horarios y direcciones físicas heterogéneas o vacías en sitios arqueológicos.
* **Qué buscaba el Objetivo del Sprint (Sprint Goal):** Entregar un recorrido web completo y verificado en Django para buscar, filtrar de forma segura (`$where` saneado) y resumir espacios culturales reales de Colombia manejando entradas vacías, cero coincidencias, datos incompletos y contingencia offline con CSV local.
* **Recorrido funcional realmente disponible:** Consulta en vivo a Socrata API (con fallback automático a `/data/cultural_spaces_sample.csv`), formulario de búsqueda por nombre, municipio, departamento y tipo de lugar, panel de resumen estadístico (total mostrados, municipios, departamentos y categorías principales) y tarjetas de resultados con atribución oficial.
* **Qué cumplió la DoD y qué quedó pendiente:** Cumple inicio sin errores (`manage.py check`), recorrido completo en navegador, datos reales con fuente identificada, manejo de entradas vacías/inválidas/sin resultados y 7 pruebas automatizadas en `tests.py`. Queda **pendiente** la revisión por un par y fusión del [Pull Request #4](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4) (`Refs #2`) y mover el [Issue #2](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/2) a `Done` tras dicha fusión.

### 8.2 Retrospectiva del Sprint (Sprint Retrospective)
* **¿Qué funcionó bien en nuestra forma de trabajar?**
  * La separación entre `views.py` y `services.py` permitió encapsular el saneamiento de `$where`, la limpieza de datos incompletos y el respaldo CSV local en funciones puras, logrando pruebas unitarias rápidas (`~0.02s`) sin requerir base de datos.
  * El uso de la clave SSH local permitió subir el repositorio y todas las ramas a GitHub sin exponer tokens ni credenciales en ningún archivo del proyecto.
* **¿Qué obstáculo afectó más el resultado?**
  * Aunque el acceso SSH a GitHub estaba activo para `git push`, el cliente `gh` CLI no tenía una sesión OAuth iniciada (`gh auth login`), por lo que la creación de Issues, Project y Pull Request requirió completarse desde la interfaz web de GitHub.
* **¿Qué acción concreta mejoraríamos en el próximo ciclo?**
  * Verificar tanto `ssh -T git@github.com` como `gh auth status` en los primeros 5 minutos del Sprint antes de iniciar el desarrollo, e incorporar paginación (`$offset`) y autocompletado de municipios en la interfaz.

---

## 9. Resumen Consolidado de Entregables (Para entrega en Moodle)

| Elemento | Evidencia verificable |
|---|---|
| **Descubrimiento** | Hipótesis de problema, usuario objetivo, exploración de 3 candidatos y justificación de `te39-v28f` en la [Sección 4](#4-fase-1--descubrimiento-del-problema). |
| **Producto** | Repositorio en https://github.com/andressantiagomeloaguirre67-sys/Hackathon y aplicación Django ejecutable con `python manage.py runserver`. |
| **Reproducibilidad** | Pasos de instalación, entorno virtual, `requirements.txt` y origen de datos en las [Secciones 1 y 2](#1-fuente-de-datos-oficial-verificada-en-apiviewste39-v28fjson). |
| **Planificación** | Product Goal, Product Backlog (3 PBIs), Sprint Goal, Sprint Backlog y DoD en las [Secciones 5 y 6](#5-planificación-ágil). |
| **Seguimiento** | Issues [#1](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/1), [#2](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/2), [#3](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/3) y tablero en https://github.com/andressantiagomeloaguirre67-sys/Hackathon/projects ([`docs/github/project.md`](docs/github/project.md)). |
| **Colaboración** | Ramas por funcionalidad (`feature/*`), commits en inglés y [Pull Request #4](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4) abierto con `Refs #2`. |
| **Calidad** | Criterios de aceptación verificados, prueba manual con `runserver` y suite automatizada (`python manage.py test -v 2` → `OK`) en la [Sección 7](#7-resultado-real-de-las-pruebas). |
| **Aprendizaje** | Sprint Review, pendientes explícitos y acción concreta de mejora en la [Sección 8](#8-fase-4--revisión-del-sprint-sprint-review-y-retrospectiva). |
