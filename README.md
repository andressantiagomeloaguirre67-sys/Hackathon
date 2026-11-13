# Directorio Ciudadano de Espacios de las Artes, las Culturas y los Saberes (Colombia)

Aplicación web construida en **Python + Django** que consulta datos abiertos reales del portal oficial [datos.gov.co](https://www.datos.gov.co/) para facilitar a la ciudadanía el descubrimiento de escenarios culturales, bibliotecas, museos, casas de cultura, escuelas de música y sitios patrimoniales en toda Colombia.

---

## 1. Descubrimiento

* **Problema (hipótesis, no hecho confirmado):** Se plantea como **hipótesis** que ciudadanos, estudiantes, turistas y gestores culturales en Colombia tienen dificultades para encontrar en un solo lugar qué espacios culturales, bibliotecas, museos o escenarios artísticos existen en su municipio o departamento, ya que la información suele estar dispersa en registros técnicos nacionales (como PULEP, SIlep, SiMCO o ICANH).
* **Usuario objetivo:** Ciudadanos, estudiantes, docentes, investigadores, turistas y gestores culturales en Colombia interesados en localizar espacios culturales y patrimoniales en su territorio.
* **Fuente de datos:**
  * **Nombre del dataset:** Espacios de las Artes, las Culturas y los Saberes (`te39-v28f`)
  * **Entidad publicadora:** Ministerio de las Culturas, las Artes y los Saberes (MinCultura) — Bogotá D.C.
  * **URL del portal:** https://www.datos.gov.co/Cultura/Espacios-de-las-Artes-las-Culturas-y-los-Saberes/te39-v28f
  * **Endpoint API Socrata:** `https://www.datos.gov.co/resource/te39-v28f.json`
  * **Volumen verificado:** 29.961 registros (última actualización verificada: `2026-11-13`).
* **Campos usados:**
  * `nombre_del_lugar`: Nombre oficial o registrado del espacio cultural.
  * `tipo_lugar`: Categoría del espacio (ej. `Biblioteca`, `Casa de Cultura`, `Museo / Entidad Museal`, `Escuela de música`, `Escenario - LEP`, `Archivo Histórico`, `Sitio Arqueológico`, etc.).
  * `departamento`: Departamento donde se ubica el espacio.
  * `municipio`: Municipio donde se ubica el espacio.
  * `direcci_n_f_sica`: Dirección física registrada del lugar.
  * `descripci_n`: Descripción del espacio y su clasificación en el registro origen.
  * `fuente`: Sistema o entidad de origen del registro (ej. `PULEP`, `Red Nacional de Bibliotecas Públicas`, `SIMCO`, `ICANH`).
* **Funcionalidad principal:** **Buscar, filtrar y resumir** espacios culturales por municipio, departamento, tipo de lugar o palabra clave en el nombre del espacio, mostrando sus detalles de ubicación, descripción y fuente oficial.
* **Limitaciones del dataset:**
  * No incluye número telefónico, correo electrónico ni horarios de atención al público.
  * Las direcciones físicas no están estandarizadas y algunos registros (especialmente sitios arqueológicos) carecen de dirección urbana detallada o descripción extensa.

---

## 2. Planificación Ágil

### Product Goal
Permitir que cualquier ciudadano o gestor cultural en Colombia descubra de forma rápida, confiable y accesible los espacios culturales, bibliotecas, museos y escenarios artísticos de su municipio o departamento utilizando datos abiertos oficiales del Ministerio de las Culturas, las Artes y los Saberes.

### Product Backlog (3 PBIs)

#### PBI #1 — Consulta de espacios culturales reales y manejo resiliente de datos (Prioridad: High)
* **Historia de usuario:** *Como* ciudadano interesado en la oferta cultural de mi territorio, *quiero* visualizar un listado claro de espacios culturales reales obtenidos de `datos.gov.co` junto con su fuente oficial, *para* conocer qué lugares culturales existen y dónde están ubicados incluso si algún registro tiene campos incompletos.
* **Criterios de aceptación comprobables:**
  1. La página principal consulta la API Socrata (`https://www.datos.gov.co/resource/te39-v28f.json`) con timeout configurado y muestra los espacios con nombre, tipo de lugar, municipio, departamento, dirección física, descripción y fuente.
  2. Si un registro carece de `direcci_n_f_sica`, `descripci_n` u otro campo opcional, la interfaz muestra un texto predeterminado legible (`"No especificada"` / `"Sin descripción disponible"`) sin romperse ni mostrar valores vacíos confusos.
  3. Si la API de `datos.gov.co` no responde por falta de conexión o timeout, el servicio utiliza automáticamente un archivo de respaldo real en `/data/cultural_spaces_sample.csv` e informa del origen de los datos.
  4. El pie de página y encabezado muestran explícitamente la atribución al Ministerio de las Culturas, las Artes y los Saberes y el enlace a `datos.gov.co`.

#### PBI #2 — Búsqueda y filtrado seguro por municipio, departamento, tipo de espacio y nombre (Prioridad: High)
* **Historia de usuario:** *Como* estudiante o gestor cultural, *quiero* buscar espacios por palabra clave y filtrar por departamento, municipio o tipo de espacio cultural, *para* encontrar rápidamente los lugares específicos que me interesan en mi localidad sin tener que revisar miles de registros.
* **Criterios de aceptación comprobables:**
  1. El formulario permite filtrar por texto en el nombre (`q`), municipio (`municipio`), departamento (`departamento`) y tipo de lugar (`tipo_lugar`), enviando una consulta Socrata (`$where` y `$limit`) correctamente construida.
  2. Todas las entradas de usuario se sanean antes de incluirse en la cláusula `$where` (escapando comillas simples `'` por `''` y limpiando espacios extremos) para evitar errores de sintaxis SoQL o inyección en la consulta.
  3. Cuando el usuario envía el formulario con entradas vacías o sin filtros activos, la aplicación tiene un comportamiento definido: muestra los primeros espacios culturales disponibles e indica que se están visualizando resultados generales.
  4. Cuando una búsqueda no arroja coincidencias (0 resultados), la aplicación muestra un mensaje claro y amigable en español indicando que no se encontraron espacios para los filtros aplicados y ofrece un enlace para limpiar la búsqueda.

#### PBI #3 — Resumen estadístico rápido de los resultados consultados (Prioridad: Medium)
* **Historia de usuario:** *Como* ciudadano o investigador cultural, *quiero* ver indicadores resumidos sobre los resultados de mi consulta (total de espacios mostrados, número de municipios representados y tipos de espacios predominantes), *para* dimensionar de un vistazo la diversidad cultural del territorio filtrado.
* **Criterios de aceptación comprobables:**
  1. Sobre la lista de resultados se muestra un panel de resumen con el total de espacios retornados en la consulta, la cantidad de municipios distintos en la muestra y el conteo por los principales tipos de espacio cultural encontrados.
  2. Si la búsqueda no devuelve resultados, el resumen refleja `0` resultados sin generar errores de cálculo ni excepciones en la plantilla.

---

### Sprint Goal
Entregar un recorrido web completo y verificado en Django que permita buscar, filtrar de forma segura y resumir espacios culturales reales de Colombia desde la API de `datos.gov.co`, manejando entradas vacías, búsquedas sin resultados, registros incompletos y contingencias de red.

### Sprint Backlog
* **Objetivo del Sprint:** Implementar y probar de extremo a extremo los 3 PBIs del Product Backlog en una aplicación Django sin base de datos propia, consumiendo directamente Socrata API con respaldo CSV.
* **PBIs seleccionados:** PBI #1 (High), PBI #2 (High), PBI #3 (Medium).
* **Plan de trabajo por ramas:**
  1. Configuración base del proyecto Django y documentación GitHub (`main`).
  2. Rama `feature/cultural-spaces-listing` (PBI #1): cliente HTTP Socrata en `services.py`, normalización de registros incompletos, respaldo CSV en `/data/`, vista inicial y plantilla con atribución.
  3. Rama `feature/search-and-filter` (PBI #2): construcción y saneamiento de consultas SoQL (`$where`), formulario de filtros en español, manejo de entrada vacía y estado sin coincidencias.
  4. Rama `feature/results-summary` (PBI #3): cálculo de resumen de resultados y pruebas automatizadas en `tests.py` para los 4 casos obligatorios con mocks HTTP.

---

## 3. Definición de Hecho (DoD)

- [ ] Django inicia sin errores.
- [ ] El recorrido se completa en el navegador.
- [ ] Datos reales con fuente identificada (`te39-v28f` - MinCultura / `datos.gov.co`).
- [ ] Criterios de aceptación cumplidos para los PBIs del Sprint.
- [ ] Entradas inválidas o resultados vacíos no rompen la app.
- [ ] Se ejecutó una prueba real (`python manage.py test` y prueba manual con `runserver`).
- [ ] Cambios revisados e integrados en `main`.
- [ ] `README.md` permite instalar y ejecutar paso a paso.
- [ ] Issues y Project reflejan el estado real (documentados en `/docs/github/` al no contar con `gh` CLI en el entorno).
