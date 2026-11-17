# Directorio Ciudadano de Espacios de las Artes, las Culturas y los Saberes (Colombia)

Aplicación web construida en **Python + Django** (sin modelos ni base de datos propia) que consume en tiempo real datos abiertos oficiales del portal [datos.gov.co](https://www.datos.gov.co/) para que ciudadanos, estudiantes y gestores culturales puedan **buscar, filtrar, resumir, recorrer por páginas y descargar** escenarios culturales, bibliotecas, museos, casas de cultura, escuelas de música, archivos históricos y sitios patrimoniales de toda Colombia.

---

## Enlaces en GitHub

* **Repositorio:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon
* **Historial de commits (`main`):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/commits/main
* **Ramas:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/branches
* **GitHub Project (tablero):** https://github.com/users/andressantiagomeloaguirre67-sys/projects/11
* **Issues (15 historias de usuario):** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues?q=is%3Aissue
* **Pull Requests revisados y fusionados:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pulls?q=is%3Apr+is%3Aclosed
  * [#4](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4) — Respuestas vacías, placeholders extendidos y límite seguro (`Refs #2`).
  * [#17](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/17) — Indicadores sobre todos los resultados, total real y muestra de respaldo representativa (`Refs #3`).
  * [#18](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/18) — Paginación con `$offset` conservando los filtros (`Refs #8`, HU-07).
  * [#19](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/19) — Descarga CSV y autocompletado de municipios sin tildes (`Refs #10`, `Refs #9`; HU-14 y HU-08).

---

## 1. Fuente de Datos Oficial

* **Conjunto de datos:** *Espacios de las Artes, las Culturas y los Saberes*
* **Identificador Socrata:** `te39-v28f`
* **Entidad publicadora:** Ministerio de las Culturas, las Artes y los Saberes - MinCultura, Bogotá D.C.
* **Autor de la tabla:** Ministerio de las Culturas, las Artes y los Saberes - Oficina de Planeación
* **Portal:** https://www.datos.gov.co/Cultura/Espacios-de-las-Artes-las-Culturas-y-los-Saberes/te39-v28f
* **Endpoint API (JSON):** `https://www.datos.gov.co/resource/te39-v28f.json`
* **Registros:** 29.966 (consultados con `count(*)` el 16 de noviembre de 2026; el 13 de noviembre eran 29.961).
* **Respaldo local sin conexión:** `/data/cultural_spaces_sample.csv` — muestra real de **351 registros de 19 tipos de espacio** (hasta 20 por tipo), descargada del mismo dataset con `scripts/download_sample.py`. No representa el conjunto completo: cuando se usa, la aplicación lo avisa en pantalla.

---

## 2. Instalación y Ejecución

### Requisitos previos
* **Python 3.12 o superior** (Django 6.1 lo exige). Verificado con Python 3.12.10 en Windows y 3.14.8 en Linux.
* Git.
* Conexión a internet para consultar la API en vivo (sin conexión, la aplicación usa la muestra local).

### Pasos

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/andressantiagomeloaguirre67-sys/Hackathon.git
   cd Hackathon
   ```

2. **Crear y activar el entorno virtual:**

   *Windows (PowerShell):*
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
   Si PowerShell bloquea la activación ("la ejecución de scripts está deshabilitada"), ejecuta una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y vuelve a activar.

   *Linux o macOS:*
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar las dependencias (versiones fijadas en `requirements.txt`):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar la configuración:**
   ```bash
   python manage.py check
   ```

5. **Ejecutar las pruebas automatizadas:**
   ```bash
   python manage.py test -v 2
   ```

6. **Iniciar el servidor:**
   ```bash
   python manage.py runserver
   ```
   Abrir en el navegador: **http://127.0.0.1:8000/**

7. **(Opcional) Regenerar la muestra de respaldo** desde la API (necesita internet; solo reemplaza el archivo si toda la descarga sale bien):
   ```bash
   python scripts/download_sample.py
   ```

---

## 3. Estructura del Proyecto

```text
.
├── config/
│   ├── settings.py          # Configuración Django sin base de datos (DATABASES = {}) y SECRET_KEY por entorno
│   ├── urls.py              # Enrutador raíz
│   ├── asgi.py / wsgi.py
├── cultural_spaces/
│   ├── services.py          # Cliente Socrata, saneamiento SoQL, normalización, respaldo CSV, resumen agregado,
│   │                        # paginación, exportación CSV y catálogo de municipios en caché
│   ├── views.py             # Vista principal (búsqueda, filtros, resumen, paginación) y descarga CSV
│   ├── urls.py              # Rutas: "/" y "/exportar-csv/"
│   ├── templates/cultural_spaces/index.html  # Interfaz en español, accesible, con atribución
│   └── tests.py             # 33 pruebas automatizadas con mocks HTTP
├── data/
│   └── cultural_spaces_sample.csv  # Muestra real del dataset para contingencia sin conexión
├── scripts/
│   └── download_sample.py   # Descarga una muestra representativa (todos los tipos de espacio)
├── docs/
│   ├── HISTORIADEUSUARIO_ISSUES.md  # Catálogo original de las 15 historias (texto de planificación)
│   └── github/
│       ├── issues.md        # Mapa de historias, issues y estado
│       ├── project.md       # Estructura y estado del GitHub Project
│       └── pull_requests.md # Pull Requests revisados y fusionados
├── manage.py
├── requirements.txt
└── README.md
```

---

## 4. Fase 1 — Descubrimiento del Problema

### 4.1 Fuentes candidatas exploradas y justificación
Se exploró el catálogo Socrata de `datos.gov.co` (`api.us.socrata.com/api/catalog/v1`), descartando fuentes con menos de 200 registros o más de 3 años sin actualizar (`rpqd-dc8v`, `ideb-ck93`, `g8hy-gwg8`, `2h8t-2zik`), y se compararon 3 candidatas:

1. `b4dp-ximh` — *Prestadores de Salud Departamento de Antioquia* (Gobernación de Antioquia, 17.232 registros, actualizado 2025-03-19).
2. **`te39-v28f` — *Espacios de las Artes, las Culturas y los Saberes* (MinCultura, 29.961 registros, actualizado 2026-11-13) — SELECCIONADA.**
3. `7tec-5fhs` — *Instituciones Educativas del Atlántico* (Gobernación del Atlántico, 212 registros, actualizado 2024-08-21).

**Justificación:** cobertura nacional, actualización reciente, volumen suficiente y columnas categóricas y geográficas claras (`departamento`, `municipio`, `tipo_lugar`, `nombre_del_lugar`) para un recorrido completo de búsqueda, filtrado y resumen.

### 4.2 Entregable del Descubrimiento
* **Nombre provisional:** *Directorio Ciudadano de Espacios de las Artes, las Culturas y los Saberes de Colombia*.
* **Problema o hipótesis de necesidad:** se plantea como **hipótesis** (no contrastada con usuarios en campo) que ciudadanos, estudiantes, turistas y gestores culturales tienen dificultad para saber en un solo lugar qué escenarios culturales, bibliotecas, museos o casas de cultura existen en su municipio o departamento, porque los registros oficiales vienen de sistemas sectoriales separados (PULEP, Red Nacional de Bibliotecas Públicas, SIMCO, ICANH, entre otros).
* **Usuario o beneficiario y decisión que le facilita:** ciudadanos, estudiantes, docentes, investigadores, turistas y gestores culturales; les ayuda a **identificar a qué espacios culturales acudir o con cuáles articular actividades** en su territorio.
* **Fuente:** [`te39-v28f`](https://www.datos.gov.co/resource/te39-v28f.json), Ministerio de las Culturas, las Artes y los Saberes - MinCultura, Bogotá D.C.
* **Campos relevantes y alcance:** `nombre_del_lugar`, `tipo_lugar`, `departamento`, `municipio`, `direcci_n_f_sica`, `descripci_n`, `fuente` y `divipola`. Alcance nacional.
* **Funcionalidad principal y valor esperado:** buscar, filtrar y resumir espacios culturales por nombre, municipio, departamento y tipo, con indicadores sobre todos los resultados de la consulta.
* **Limitaciones de los datos:**
  * No incluye teléfono, correo ni horarios.
  * Direcciones no estandarizadas; algunas traen textos como "SIN REGISTRO".
  * Los **sitios arqueológicos** (ICANH), que son la mayoría de los registros (18.236), vienen **sin descripción ni dirección**; la interfaz lo indica con "Sin descripción disponible" y "No especificada".
  * Muchos sitios arqueológicos tienen nombres que empiezan por un código numérico ("011 Indro"), por eso aparecen primero en el orden alfabético.
  * La fuente reporta **34 departamentos distintos** (Colombia tiene 33 contando Bogotá), probablemente por nombres escritos de dos formas.
  * El dataset tiene **19 tipos de espacio**; el filtro de tipo ofrece los 10 principales y los demás se encuentran buscando por nombre.
* **Riesgos de implementación y mitigación:** caída o lentitud de la API (timeout de 8 segundos y respaldo CSV local), errores o inyección SoQL por caracteres especiales (saneamiento en `sanitize_soql_value`) y la API no ignora tildes (catálogo de municipios oficiales, ver HU-08).

---

## 5. Planificación Ágil

### Product Goal
Permitir que cualquier ciudadano o gestor cultural en Colombia descubra de forma rápida, confiable y accesible los espacios culturales de su municipio o departamento, utilizando datos abiertos oficiales del Ministerio de las Culturas, las Artes y los Saberes.

### Sprint Goal
Entregar un recorrido web completo y verificado en Django que permita buscar, filtrar de forma segura y resumir espacios culturales reales de Colombia desde la API de `datos.gov.co`, manejando entradas vacías, búsquedas sin resultados, registros incompletos y fallos de red.

### Product Backlog

El Product Backlog está en GitHub como **15 historias de usuario** (issues) en el [GitHub Project](https://github.com/users/andressantiagomeloaguirre67-sys/projects/11), ordenadas por prioridad (campo `Priority`: **P0** = alta, **P1** = media, **P2** = baja). El Sprint se planificó con **3 PBIs** (issues #1, #2 y #3); las otras 12 historias desglosan esos PBIs o representan la evolución del producto. El mapa completo de historias, issues, responsables y estado está en [`docs/github/issues.md`](docs/github/issues.md).

#### PBI #1 — Consulta de espacios culturales reales con manejo resiliente de datos (P0) · [Issue #1](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/1)
* **Historia de usuario:** *Como* ciudadano interesado en la oferta cultural de mi territorio, *quiero* ver un listado claro de espacios culturales reales de `datos.gov.co` con su fuente oficial, *para* saber qué lugares existen y dónde están, aunque algún registro tenga campos incompletos.
* **Criterios de aceptación:**
  1. Consulta `https://www.datos.gov.co/resource/te39-v28f.json` con timeout de 8 segundos y muestra nombre, tipo, municipio, departamento, dirección, descripción y registro de origen.
  2. Los campos ausentes o con marcadores (`"Sin Dato"`, `"No registra"`…) se muestran con textos claros (`"No especificada"`, `"Sin descripción disponible"`) sin romper la interfaz.
  3. Si falla la API, usa automáticamente `/data/cultural_spaces_sample.csv` y avisa en pantalla que es una muestra.
  4. Muestra la atribución al Ministerio de las Culturas, las Artes y los Saberes y el enlace a `datos.gov.co`.
* **Historias que lo desglosan:** HU-01, HU-05, HU-06, HU-09.

#### PBI #2 — Búsqueda y filtrado seguro por nombre, municipio, departamento y tipo (P0) · [Issue #2](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/2)
* **Historia de usuario:** *Como* estudiante o gestor cultural, *quiero* buscar por palabra clave y filtrar por departamento, municipio o tipo de espacio, *para* encontrar rápido los lugares que me interesan sin revisar miles de registros.
* **Criterios de aceptación:**
  1. Formulario con `q` (nombre), `municipio`, `departamento` y `tipo_lugar` que construye la cláusula `$where` de Socrata.
  2. `sanitize_soql_value` escapa comillas simples (`'` → `''`), quita caracteres de control y limita la longitud antes de armar `$where`.
  3. **Entrada vacía:** al enviar el formulario vacío o con espacios, muestra el listado general y avisa que no hay filtros.
  4. **Sin coincidencias:** muestra un mensaje claro en español, los filtros aplicados y un botón para limpiarlos.
* **Historias que lo desglosan:** HU-02, HU-04, HU-10; ampliado en este Sprint con HU-07 (paginación), HU-08 (municipios sin tildes) y HU-14 (descarga CSV).

#### PBI #3 — Resumen estadístico de los resultados consultados (P1) · [Issue #3](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/3)
* **Historia de usuario:** *Como* ciudadano o investigador cultural, *quiero* ver indicadores sobre los resultados de mi consulta (total de espacios, municipios y departamentos, y tipos predominantes), *para* dimensionar de un vistazo la oferta cultural del territorio filtrado.
* **Criterios de aceptación:**
  1. Tarjetas de resumen con el total de espacios encontrados, municipios, departamentos y las 4 categorías principales, calculados sobre **todos** los resultados que coinciden.
  2. Con 0 resultados, los indicadores muestran `0` sin errores.
  3. Si las consultas agrupadas fallan, los indicadores se calculan sobre los registros listados y la página lo indica.
* **Historias que lo desglosan:** HU-03; con soporte transversal de HU-11 (interfaz accesible), HU-12 (pruebas) y HU-13 (configuración).

#### Orden del Product Backlog completo
| Prioridad | Historias |
|---|---|
| P0 (alta) | HU-01 Consulta API · HU-02 Búsqueda y filtros · HU-04 Saneamiento SoQL · HU-05 Datos incompletos · HU-06 Respaldo CSV · HU-10 Estados de búsqueda · HU-12 Pruebas |
| P1 (media) | HU-03 Resumen · HU-07 Paginación · HU-09 Atribución y fuente activa · HU-11 Interfaz accesible · HU-13 Configuración sin estado · HU-14 Descarga CSV |
| P2 (baja) | HU-08 Autocompletado y tildes · HU-15 Enlace a mapa |

### Sprint Backlog: plan de implementación

El Sprint Backlog es el **Sprint Goal** (arriba) + los **PBIs #1, #2 y #3** + este plan:

| Trabajo | Historias | Responsable | Dependencias | Verificación |
|---|---|---|---|---|
| Configuración base de Django sin base de datos, dependencias fijadas y `.gitignore` | HU-13 | Andres | Ninguna | `python manage.py check` sin problemas |
| Cliente Socrata, normalización de datos ausentes, respaldo CSV y atribución | HU-01, HU-05, HU-06, HU-09 | Andres | Configuración base | Pruebas de datos incompletos y de caída de red; revisión en el navegador |
| Búsqueda y filtros con `$where` saneado, entrada vacía y sin coincidencias | HU-02, HU-04, HU-10 | Andres (código base); mejoras en [PR #4](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4), revisado por Juliana | Cliente Socrata y normalizador | Pruebas de inyección SoQL, entrada vacía y cero resultados (7 OK) |
| Indicadores sobre todos los resultados, total real y muestra representativa | HU-03, HU-06, HU-09, HU-12 | Juliana — [PR #17](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/17), revisado por Andres | Filtros (`build_soql_where`) para reutilizar el mismo `$where` | 13 pruebas OK; Antioquia: 7.559 espacios y 125 municipios |
| Paginación con `$offset` conservando filtros | HU-07 | Andres — [PR #18](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/18), revisado por Juliana | Indicadores del PR #17 (total para calcular las páginas) | 19 pruebas OK; navegación página 1 → 2 → 3 con filtros |
| Descarga CSV y autocompletado de municipios sin tildes | HU-14, HU-08 | Juliana — [PR #19](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/19), revisado por Andres | Filtros y paginación (mismo orden y `$where`) | 33 pruebas OK; CSV abierto en Excel; "medellin" encuentra Medellín |
| Interfaz responsiva y accesible | HU-11 | Andres (base); ampliada en PR #18 y PR #19 | Plantilla `index.html` | Revisión de etiquetas, ARIA y diseño en móvil y escritorio |

**Cambio en el equipo:** el plan inicial asignaba historias a Andres, Juliana y Santiago. Santiago aportó un enlace a una carpeta de historias en el README (commit `a3fd161`); el trabajo pendiente se redistribuyó entre Andres y Juliana, y HU-14 se reasignó a Juliana.

**Pendiente para el siguiente ciclo:** HU-15 (enlace a mapa con coordenadas), en Backlog.

### Ramas y commits
* Ramas de funcionalidad: `feature/cultural-spaces-listing`, `feature/search-and-filter`, `feature/results-summary`, `feature/improve-empty-states`, y las ramas de trabajo `Andres` y `Juliana`.
* Mensajes de commit en inglés con referencia a la historia (`Refs #N` o `Refs HU-XX`). Historial completo: https://github.com/andressantiagomeloaguirre67-sys/Hackathon/commits/main
* Los commits `da4fb8f`, `6bb0932` y `9e58bff` ("Merge pull request #1/#2/#3") son fusiones locales de las ramas iniciales; no corresponden a Pull Requests de GitHub. Los Pull Requests reales son #4, #17, #18 y #19.

---

## 6. Definición de Terminado (DoD) — Estado Real

- [x] **Django inicia sin errores:** `python manage.py check` → `System check identified no issues (0 silenced)`.
- [x] **El recorrido principal se completa en el navegador:** búsqueda, filtros, resumen, paginación, descarga CSV y sugerencias de municipio, probados con `runserver` y la API real.
- [x] **La aplicación atiende el problema de forma demostrable:** permite ubicar los espacios culturales de un municipio o departamento y dimensionar la oferta con indicadores.
- [x] **Datos reales con fuente identificada:** API `te39-v28f` en vivo, con atribución a MinCultura en el encabezado, el pie de página, cada tarjeta y el CSV descargado.
- [x] **Criterios de aceptación cumplidos:** marcados en las 14 historias terminadas en GitHub.
- [x] **Entradas inválidas o resultados vacíos no rompen la aplicación:** entradas en blanco, comillas simples, búsquedas sin coincidencias, páginas inválidas o fuera de rango, registros con `"Sin Dato"` y caída de la API.
- [x] **Se ejecutó y registró una comprobación funcional real:** pruebas automatizadas (sección 7.1) y prueba manual (sección 7.2).
- [x] **Cambios revisados e integrados en `main`:** PRs #4, #17, #18 y #19, cada uno revisado y aprobado por un integrante distinto al autor.
- [x] **El README permite instalar y ejecutar:** sección 2, con pasos para Windows y Linux.
- [x] **Issues y Project reflejan el estado verdadero:** 14 historias en Done con criterios marcados y HU-15 en Backlog.

---

## 7. Resultado Real de las Pruebas

### 7.1 Pruebas automatizadas en `main` (después de fusionar el PR #19)
```text
Found 33 test(s).
Skipping setup of unused database(s): default.
System check identified no issues (0 silenced).
test_aggregate_failure_falls_back_to_listed_page_and_count ... ok
test_all_extra_queries_failing_still_renders_listed_results ... ok
test_api_failure_falls_back_to_local_csv ... ok
test_empty_input_submission_has_defined_behavior ... ok
test_export_csv_downloads_filtered_results_with_spanish_headers ... ok
test_export_csv_neutralizes_spreadsheet_formulas ... ok
test_export_csv_uses_local_sample_when_api_fails ... ok
test_export_csv_with_no_matches_returns_only_headers ... ok
test_extended_placeholders_and_invalid_limit_are_handled_safely ... ok
test_fallback_explains_it_is_a_sample ... ok
test_fallback_filter_ignores_accents ... ok
test_fallback_results_are_sorted_by_name_like_the_api ... ok
test_fallback_sample_is_paginated_too ... ok
test_incomplete_record_does_not_break_interface ... ok
test_index_renders_datalist_for_selected_department ... ok
test_index_shows_download_button_with_current_filters ... ok
test_invalid_page_values_fall_back_to_first_page ... ok
test_municipality_field_is_an_accessible_combobox ... ok
test_municipality_matches_respect_selected_department ... ok
test_municipality_without_accent_finds_official_name ... ok
test_no_matches_renders_clear_empty_message ... ok
test_normal_search_renders_matching_spaces_and_summary ... ok
test_official_names_with_quotes_are_escaped ... ok
test_page_beyond_last_shows_clear_message ... ok
test_second_page_sends_offset_and_keeps_filters_in_links ... ok
test_short_last_page_disables_next_button ... ok
test_short_last_page_knows_total_without_count_query ... ok
test_small_result_set_does_not_request_count ... ok
test_soql_where_sanitizes_single_quotes_and_injection ... ok
test_summary_covers_all_matching_records_not_only_listed_page ... ok
test_catalog_falls_back_to_sample_without_caching_the_failure ... ok
test_catalog_uses_grouped_query_and_is_cached ... ok
test_department_keys_ignore_accents_and_punctuation ... ok

----------------------------------------------------------------------
Ran 33 tests in 0.101s

OK
```

Evolución de la suite: 6 pruebas iniciales → 7 (PR #4) → 13 (PR #17) → 19 (PR #18) → 33 (PR #19).

### 7.2 Prueba manual con `runserver` y la API real
| Caso | Resultado observado |
|---|---|
| Inicio sin filtros | 29.966 espacios, 1.114 municipios, 34 departamentos; categorías: Sitio Arqueológico 18.236, Escenario - LEP 2.055, Biblioteca 1.568, Archivo Histórico 1.369 |
| Filtro Antioquia | 7.559 espacios y 125 municipios (todos los del departamento) |
| Paginación (Antioquia) | Página 1 → 2 → 3 y regreso; "registros 41 a 80 (página 2 de 189)"; el filtro se mantiene |
| Descarga CSV (Antioquia) | Aviso "primeros 1.000 de 7.559"; el archivo abre en Excel con columnas en español y tildes correctas |
| Municipio sin tilde | "medel" sugiere Medellín; al elegir Antioquia la lista muestra solo sus municipios; "medellin" encuentra resultados |
| Entrada vacía, sin coincidencias y comillas simples | Mensajes claros, sin errores |

---

## 8. Fase 4 — Revisión del Sprint y Retrospectiva

### 8.1 Revisión del Sprint (Sprint Review)
* **Problema o hipótesis y para quién:** dispersión de la información sobre la oferta cultural en Colombia, para ciudadanos, estudiantes, investigadores y gestores culturales (hipótesis no contrastada con usuarios).
* **Fuente y limitaciones observadas:** `te39-v28f` de MinCultura (29.966 registros); limitaciones descritas en la sección 4.2.
* **Qué buscaba el Sprint Goal:** un recorrido completo y verificado para buscar, filtrar de forma segura y resumir espacios culturales reales, resistente a entradas vacías, cero coincidencias, datos incompletos y fallos de red.
* **Recorrido funcional disponible:** búsqueda por nombre, municipio (con sugerencias y sin depender de tildes), departamento y tipo; indicadores calculados sobre todos los resultados; paginación de 40 en 40; descarga CSV de hasta 1.000 registros; respaldo automático con muestra local y atribución oficial.
* **Qué cumplió la DoD y qué quedó pendiente:** cumplen la DoD las 14 historias en Done (sección 6). Queda pendiente HU-15 (enlace a mapa), en Backlog para el siguiente ciclo.
* **Resultado de la revisión (retroalimentación recibida):** *pendiente de registrar después de la demostración.*

### 8.2 Retrospectiva del Sprint
* **¿Qué funcionó bien?**
  * Separar `views.py` y `services.py` permitió probar el saneamiento, el respaldo y los cálculos con pruebas rápidas (menos de 1 segundo) sin base de datos.
  * Trabajar con Pull Requests revisados por otra persona: las revisiones encontraron mejoras reales (por ejemplo, una prueba del PR #4 que no verificaba el bloque que decía probar, corregida en el PR #17).
* **¿Qué obstáculo afectó más el resultado?**
  * Las ramas locales desactualizadas frente a `main`: varias veces hubo que actualizar ramas o reinstalar el entorno antes de poder revisar o aplicar un cambio. También la reorganización del trabajo cuando el equipo pasó de tres a dos integrantes.
* **Acción concreta para el próximo ciclo:**
  * Antes de empezar o revisar cualquier cambio, ejecutar `git fetch origin`, actualizar la rama con `git merge origin/main` y correr `python manage.py test`; si las pruebas no dan el número esperado, no se continúa hasta resolverlo.

---

## 9. Resumen de Entregables (para la entrega en Moodle)

| Elemento | Evidencia |
|---|---|
| **Descubrimiento** | Hipótesis, beneficiario, candidatas y justificación de `te39-v28f` en la [sección 4](#4-fase-1--descubrimiento-del-problema). |
| **Producto** | Repositorio https://github.com/andressantiagomeloaguirre67-sys/Hackathon y aplicación ejecutable con `python manage.py runserver`. |
| **Reproducibilidad** | Instalación para Windows y Linux, dependencias fijadas y origen de los datos en las [secciones 1 y 2](#1-fuente-de-datos-oficial). |
| **Planificación** | Product Goal, Sprint Goal, Product Backlog, Sprint Backlog y DoD en las [secciones 5 y 6](#5-planificación-ágil). |
| **Seguimiento** | [GitHub Project](https://github.com/users/andressantiagomeloaguirre67-sys/projects/11) y [issues](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues?q=is%3Aissue) con estados actualizados. |
| **Colaboración** | Ramas, commits en inglés y PRs [#4](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4), [#17](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/17), [#18](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/18) y [#19](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/19), revisados e integrados. |
| **Calidad** | Criterios de aceptación marcados en los issues y 33 pruebas reales en la [sección 7](#7-resultado-real-de-las-pruebas). |
| **Aprendizaje** | Revisión del Sprint, pendientes y acción de mejora en la [sección 8](#8-fase-4--revisión-del-sprint-y-retrospectiva). |

---

## Recursos adicionales
* **Carpeta de historias de usuario en Google Drive** (aportada por Santiago): https://drive.google.com/drive/folders/1EOStrErIt2PW49ar5Wz6jsKu1uMmVMEp — material complementario; la versión oficial y actualizada de las historias está en los issues de GitHub.
