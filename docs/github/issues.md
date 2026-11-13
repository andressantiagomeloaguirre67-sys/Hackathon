# Issues del Product Backlog (Listos para copiar en GitHub)

---

## Issue #1: Consulta de espacios culturales reales y manejo resiliente de datos

* **Estado en Project:** `Done` (verificado con DoD e integrado en `main` vía PR #1 — `Refs #1`)
* **Prioridad (`Priority`):** `High`
* **Etiquetas sugeridas:** `feature`, `pbi-1`, `high-priority`

### Contexto
Los ciudadanos y gestores culturales necesitan consultar en una interfaz web clara los registros oficiales del dataset **Espacios de las Artes, las Culturas y los Saberes (`te39-v28f`)** publicado por el Ministerio de las Culturas, las Artes y los Saberes en `datos.gov.co`. Dado que se trata de una fuente externa de datos abiertos donde algunos registros tienen campos vacíos y pueden existir fallos de conectividad, el servicio debe normalizar los datos incompletos y contar con un respaldo CSV local real en `/data/`.

### Historia de Usuario
> **Como** ciudadano interesado en la oferta cultural de mi territorio,  
> **quiero** visualizar un listado claro de espacios culturales reales obtenidos de `datos.gov.co` junto con su fuente oficial,  
> **para** conocer qué lugares culturales existen y dónde están ubicados incluso si algún registro tiene campos incompletos.

### Criterios de Aceptación
- [x] La página principal consulta `https://www.datos.gov.co/resource/te39-v28f.json` con un `timeout` explícito y muestra cada espacio con su nombre, tipo de lugar, municipio, departamento, dirección física, descripción y fuente.
- [x] Si un registro viene con campos faltantes o vacíos (ej. sin `direcci_n_f_sica` o sin `descripci_n`), la aplicación asigna valores por defecto claros (`"No especificada"`, `"Sin descripción disponible"`) y la interfaz no se rompe.
- [x] Si ocurre un error de conexión o timeout al consultar la API Socrata, el servicio carga automáticamente datos reales de respaldo desde `/data/cultural_spaces_sample.csv` y notifica el origen en la interfaz.
- [x] La página incluye atribución visible al Ministerio de las Culturas, las Artes y los Saberes y enlace directo a `datos.gov.co`.

---

## Issue #2: Búsqueda y filtrado seguro por municipio, departamento, tipo de espacio y nombre

* **Estado en Project:** `Done` (verificado con DoD e integrado en `main` vía PR #2 — `Refs #2`)
* **Prioridad (`Priority`):** `High`
* **Etiquetas sugeridas:** `feature`, `pbi-2`, `high-priority`, `security`

### Contexto
El dataset `te39-v28f` cuenta con 29.961 registros en toda Colombia. Para que el directorio sea útil a un ciudadano, debe permitir filtrar por ubicación (`departamento`, `municipio`), por categoría (`tipo_lugar`) y por palabra clave en el nombre del espacio (`nombre_del_lugar`) mediante consultas SoQL (`$where`). Es indispensable sanear cualquier texto ingresado por el usuario antes de construir la cláusula `$where` para evitar errores o inyección SoQL.

### Historia de Usuario
> **Como** estudiante o gestor cultural,  
> **quiero** buscar espacios por palabra clave y filtrar por departamento, municipio o tipo de espacio cultural,  
> **para** encontrar rápidamente los lugares específicos que me interesan en mi localidad sin tener que revisar miles de registros.

### Criterios de Aceptación
- [x] El formulario HTML permite buscar por nombre y filtrar por departamento, municipio y tipo de lugar.
- [x] La función de servicio sanea las entradas del usuario escapando comillas simples (`'` -> `''`) y eliminando caracteres de control antes de construir el parámetro `$where`.
- [x] **Entrada vacía:** Si el usuario envía el formulario vacío o ingresa solo espacios en blanco, la aplicación muestra el listado general inicial con un comportamiento definido y sin errores.
- [x] **Sin coincidencias:** Si la búsqueda devuelve una lista vacía (`[]`), la interfaz presenta un mensaje claro en español informando que no se hallaron coincidencias y un botón para restablecer los filtros.

---

## Issue #3: Resumen estadístico rápido de los resultados consultados

* **Estado en Project:** `Done` (verificado con DoD e integrado en `main` vía PR #3 — `Refs #3`)
* **Prioridad (`Priority`):** `Medium`
* **Etiquetas sugeridas:** `feature`, `pbi-3`, `medium-priority`

### Contexto
Además del listado individual de espacios culturales, mostrar un resumen cuantitativo de los resultados actuales (total de espacios mostrados, cantidad de municipios distintos y desglose por tipos de lugar predominantes) ayuda al usuario a comprender rápidamente la oferta cultural encontrada en su búsqueda.

### Historia de Usuario
> **Como** ciudadano o investigador cultural,  
> **quiero** ver indicadores resumidos sobre los resultados de mi consulta (total de espacios mostrados, número de municipios representados y tipos de espacios predominantes),  
> **para** dimensionar de un vistazo la diversidad cultural del territorio filtrado.

### Criterios de Aceptación
- [x] La interfaz muestra tarjetas de resumen con el total de espacios retornados, total de municipios y departamentos representados en la vista actual, y las principales categorías (`tipo_lugar`) con su conteo.
- [x] Cuando la búsqueda no arroja resultados (0 coincidencias), el resumen se calcula de forma segura mostrando valores en cero sin provocar errores en la vista ni en el template.
- [x] Existen pruebas automatizadas en `tests.py` (con mocks HTTP) que verifican búsqueda normal, búsqueda sin coincidencias, entrada vacía, dato incompleto y saneamiento de `$where`.
