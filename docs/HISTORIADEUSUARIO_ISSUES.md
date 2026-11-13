# Catálogo Completo de Historias de Usuario e Issues (Product Backlog)

Documento elaborado con enfoque de ingeniería de software ágil (Scrum) que desglosa de forma atómica e independiente todas las **Historias de Usuario (HU-01 a HU-08)** del *Directorio Ciudadano de Espacios de las Artes, las Culturas y los Saberes de Colombia*.

Cada Historia de Usuario cumple los criterios **INVEST** (*Independent, Negotiable, Valuable, Estimable, Small, Testable*) y está lista para copiarse directamente como **Issue en GitHub**, permitiendo poblar de manera coherente todas las columnas del **GitHub Project** (`Backlog`, `Ready`, `In Progress`, `In Review`, `Done`) y distribuir responsabilidades entre el equipo (`Andres`, `Santiago`, `Juliana`).

---

## Mapa General de Historias de Usuario y Tablero GitHub Project

| ID | Título para GitHub Issue | Prioridad (`Priority`) | Responsable sugerido | Rama / Evidencia técnica | Columna en GitHub Project (`Status`) |
|---|---|---|---|---|---|
| **HU-01** *(Issue #1)* | `HU-01: Consulta inicial de espacios culturales reales y atribución oficial de datos.gov.co` | `High` | `Andres` | `feature/cultural-spaces-listing` (`services.py`, `views.py`, `index.html`) | `Done` |
| **HU-02** *(Issue #2)* | `HU-02: Búsqueda por palabra clave y filtrado combinado por departamento, municipio y tipo` | `High` | `Santiago` | `feature/search-and-filter` + `feature/improve-empty-states` (`PR #4`) | `In Review` |
| **HU-03** *(Issue #3)* | `HU-03: Resumen estadístico rápido de la oferta cultural en la consulta actual` | `Medium` | `Juliana` | `feature/results-summary` (`summarize_spaces` en `services.py`) | `Done` |
| **HU-04** *(Nuevo Issue)* | `HU-04: Saneamiento de entradas contra inyección SoQL ($where) y manejo de búsquedas en blanco` | `High` | `Santiago` | `feature/search-and-filter` (`sanitize_soql_value`, `tests.py`) | `Done` |
| **HU-05** *(Nuevo Issue)* | `HU-05: Normalización de registros con datos incompletos y retroalimentación en búsquedas sin coincidencias` | `High` | `Juliana` | `feature/improve-empty-states` (`normalize_space_record`, `index.html`, `PR #4`) | `In Review` |
| **HU-06** *(Nuevo Issue)* | `HU-06: Contingencia automática con respaldo CSV local ante caídas o timeouts de la API Socrata` | `Medium` | `Andres` | `feature/cultural-spaces-listing` (`load_fallback_csv`, `/data/cultural_spaces_sample.csv`) | `Done` |
| **HU-07** *(Nuevo Issue)* | `HU-07: Paginación de resultados ($offset y $limit) para explorar más de 40 espacios por consulta` | `Medium` | `Andres` | Planificado para siguiente iteración (Sprint 2) | `Ready` |
| **HU-08** *(Nuevo Issue)* | `HU-08: Autocompletado dinámico de municipios según el departamento seleccionado` | `Low` | `Juliana` | Planificado en Product Backlog (Sprint 2) | `Backlog` |

---

## Textos Listos para Copiar y Pegar en GitHub Issues

> **Nota:** Las historias **HU-01, HU-02 y HU-03** corresponden a los Issues `#1`, `#2` y `#3` que ya creaste en GitHub. A continuación tienes las **5 Historias de Usuario adicionales (HU-04 a HU-08)** listas para copiar y pegar en `https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/new` (también se incluyen HU-01 a HU-03 por completitud del documento).

---

### HU-01 (Ya creada como Issue #1)

**Add a title:**
```text
HU-01: Consulta inicial de espacios culturales reales y atribución oficial de datos.gov.co
```

**Add a description:**
```markdown
**Prioridad:** High  
**Responsable:** Andres  
**Estado en Project:** Done

### Contexto y Propósito
Los ciudadanos, estudiantes y gestores culturales carecen de un punto único y sencillo para consultar los registros oficiales del dataset **Espacios de las Artes, las Culturas y los Saberes (`te39-v28f`)** publicado por el Ministerio de las Culturas, las Artes y los Saberes en `datos.gov.co`. Se requiere una vista principal que consulte la API Socrata en tiempo real y muestre de forma transparente la atribución de la fuente pública.

### Historia de Usuario
> **Como** ciudadano interesado en la oferta cultural de mi país,  
> **quiero** visualizar un listado claro de espacios culturales reales obtenidos de `datos.gov.co` junto con su entidad publicadora y enlace oficial,  
> **para** conocer qué escenarios culturales, bibliotecas o museos existen y confiar en la procedencia pública de la información.

### Criterios de Aceptación
- [x] La aplicación consulta el endpoint `https://www.datos.gov.co/resource/te39-v28f.json` con `timeout=8` segundos.
- [x] Cada tarjeta de resultado presenta: nombre del espacio (`nombre_del_lugar`), categoría (`tipo_lugar`), municipio (`municipio`), departamento (`departamento`), dirección física (`direcci_n_f_sica`), descripción (`descripci_n`) y registro de origen (`fuente`).
- [x] El encabezado y el pie de página muestran explícitamente la atribución a `Ministerio de las Culturas, las Artes y los Saberes - MinCultura, Bogotá D.C.` y el enlace directo al dataset `te39-v28f`.
```

---

### HU-02 (Ya creada como Issue #2)

**Add a title:**
```text
HU-02: Búsqueda por palabra clave y filtrado combinado por departamento, municipio y tipo
```

**Add a description:**
```markdown
**Prioridad:** High  
**Responsable:** Santiago  
**Estado en Project:** In Review (Refs PR #4)

### Contexto y Propósito
Dado que el conjunto de datos `te39-v28f` contiene 29.961 registros en toda Colombia, mostrar únicamente un listado general impide que un usuario localice los espacios de su territorio. Se requiere un formulario web que combine búsqueda por texto en el nombre y filtros geográficos/categóricos mediante consultas SoQL (`$where`).

### Historia de Usuario
> **Como** estudiante, turista o gestor cultural,  
> **quiero** buscar espacios por palabra clave en el nombre y filtrar por departamento, municipio y tipo de espacio cultural,  
> **para** localizar rápidamente las bibliotecas, museos, casas de cultura o escenarios específicos de mi municipio sin revisar miles de registros.

### Criterios de Aceptación
- [x] El formulario HTML permite ingresar nombre (`q`), municipio (`municipio`) y seleccionar departamento (`departamento`) y tipo de espacio (`tipo_lugar`).
- [x] La capa de servicios (`build_soql_where`) construye dinámicamente la cláusula `$where` combinando con `AND` únicamente los filtros activos (insensible a mayúsculas/minúsculas mediante `upper(...)`).
- [x] Los valores seleccionados por el usuario se mantienen visibles en los campos del formulario tras ejecutar la búsqueda y existe un botón `"Limpiar filtros"` para restablecer la vista inicial.
```

---

### HU-03 (Ya creada como Issue #3)

**Add a title:**
```text
HU-03: Resumen estadístico rápido de la oferta cultural en la consulta actual
```

**Add a description:**
```markdown
**Prioridad:** Medium  
**Responsable:** Juliana  
**Estado en Project:** Done

### Contexto y Propósito
Además de revisar fichas individuales de espacios culturales, un investigador o gestor cultural necesita dimensionar de un vistazo cuántos espacios arrojó su búsqueda, en cuántos municipios/departamentos se distribuyen y cuáles son las categorías culturales predominantes.

### Historia de Usuario
> **Como** investigador o gestor cultural,  
> **quiero** visualizar indicadores resumidos sobre los resultados de mi consulta (total de espacios mostrados, municipios, departamentos y categorías principales),  
> **para** comprender rápidamente la composición y diversidad de la infraestructura cultural del territorio filtrado.

### Criterios de Aceptación
- [x] La función `summarize_spaces` calcula sobre los resultados actuales: `total_count`, `unique_municipalities`, `unique_departments` y el top 4 de `tipo_lugar` (`top_types`).
- [x] La interfaz muestra una barra de 4 tarjetas de resumen antes del listado de espacios culturales.
- [x] Si la consulta devuelve 0 resultados, los contadores muestran `0` y el texto `"Sin categorías para mostrar"` sin lanzar excepciones.
```

---

### HU-04 (Copiar y pegar como nuevo Issue en GitHub)

**Add a title:**
```text
HU-04: Saneamiento de entradas contra inyección SoQL ($where) y manejo de búsquedas en blanco
```

**Add a description:**
```markdown
**Prioridad:** High  
**Responsable:** Santiago  
**Estado en Project:** Done

### Contexto y Propósito
Cuando se interpolan cadenas ingresadas por el usuario dentro de una cláusula `$where` de la API Socrata (ej. `upper(nombre_del_lugar) like upper('%...%')`), una comilla simple (`'`) como en `"Teatro O'Higgins"` o una cadena maliciosa como `' OR '1'='1` rompe la sintaxis SoQL o altera la lógica de la consulta. Asimismo, los usuarios pueden enviar el formulario con espacios en blanco o parámetros vacíos.

### Historia de Usuario
> **Como** usuario de la aplicación web,  
> **quiero** que mis búsquedas con caracteres especiales (como apóstrofes) o envíos con campos en blanco sean procesados de forma segura y predecible,  
> **para** no recibir errores técnicos del servidor ni comprometer la seguridad de las consultas a la API pública.

### Criterios de Aceptación
- [x] La función `sanitize_soql_value` elimina caracteres no imprimibles, recorta espacios extremos, limita la longitud a 100 caracteres y escapa comillas simples (`'` -> `''`) antes de construir `$where`.
- [x] La función `clamp_limit` asegura que el límite de registros (`$limit`) esté siempre acotado entre `1` y `100`.
- [x] Si el usuario envía el formulario vacío o solo con espacios en blanco (`?q=   &municipio=`), no se envía parámetro `$where`, se muestra el listado general y se despliega el aviso informativo: `"Mostrando el listado general de espacios culturales (no se ingresaron filtros de búsqueda)."`.
- [x] Existe prueba unitaria automatizada (`test_soql_where_sanitizes_single_quotes_and_injection` y `test_empty_input_submission_has_defined_behavior`) verificada con `manage.py test`.
```

---

### HU-05 (Copiar y pegar como nuevo Issue en GitHub)

**Add a title:**
```text
HU-05: Normalización de registros con datos incompletos y retroalimentación en búsquedas sin coincidencias
```

**Add a description:**
```markdown
**Prioridad:** High  
**Responsable:** Juliana  
**Estado en Project:** In Review (Refs PR #4)

### Contexto y Propósito
En los conjuntos de datos abiertos gubernamentales es frecuente encontrar registros con columnas ausentes (`None`), cadenas vacías (`""`) o textos comodín como `"Sin Dato"`, `"Sin información"`, `"No registra"` o `"No aplica"`. Además, cuando una combinación de filtros no arroja resultados, el usuario necesita saber con claridad qué criterios aplicó y cómo volver al listado completo.

### Historia de Usuario
> **Como** ciudadano que consulta el directorio cultural,  
> **quiero** que los espacios con campos faltantes se muestren con textos claros por defecto y que las búsquedas sin resultados me indiquen qué filtros no tuvieron coincidencias,  
> **para** tener una experiencia de lectura limpia sin pantallas rotas ni valores técnicos confusos (`None` o `null`).

### Criterios de Aceptación
- [x] `normalize_space_record` transforma cualquier valor nulo, vacío o placeholder (`"Sin Dato"`, `"Sin información"`, `"No registra"`, `"No aplica"`, `"N/A"`) en textos legibles en español (`"Nombre no disponible"`, `"Sin clasificar"`, `"No especificado"`, `"No especificada"`, `"Sin descripción disponible"`, `"No registrada"`).
- [x] Cuando una consulta retorna 0 registros (`spaces == []`), la interfaz muestra un bloque de estado vacío claro en español detallando los filtros aplicados (`Nombre`, `Municipio`, `Departamento`, `Tipo`) y un botón `"Ver todos los espacios"`.
- [x] Cubierto por las pruebas automatizadas `test_incomplete_record_does_not_break_interface`, `test_no_matches_renders_clear_empty_message` y `test_extended_placeholders_and_invalid_limit_are_handled_safely` en `cultural_spaces/tests.py`.
```

---

### HU-06 (Copiar y pegar como nuevo Issue en GitHub)

**Add a title:**
```text
HU-06: Contingencia automática con respaldo CSV local ante caídas o timeouts de la API Socrata
```

**Add a description:**
```markdown
**Prioridad:** Medium  
**Responsable:** Andres  
**Estado en Project:** Done

### Contexto y Propósito
Toda aplicación web que depende de una API externa pública (`datos.gov.co`) está expuesta a intermitencias de red, lentitud o caídas temporales del servicio. Siguiendo las reglas de contingencia del proyecto, la aplicación debe conmutar automáticamente a una muestra real en CSV del mismo conjunto de datos almacenada en `/data/cultural_spaces_sample.csv` sin interrumpir el recorrido del usuario.

### Historia de Usuario
> **Como** ciudadano o evaluador que utiliza la aplicación cuando el portal `datos.gov.co` presenta fallos de conexión,  
> **quiero** que el sistema cargue y filtre automáticamente una muestra local real del mismo conjunto de datos advirtiendo de la contingencia,  
> **para** poder completar mi búsqueda de espacios culturales incluso sin conectividad hacia la API externa.

### Criterios de Aceptación
- [x] El repositorio incluye `/data/cultural_spaces_sample.csv` descargado directamente del conjunto oficial `te39-v28f`.
- [x] Si `requests.get` lanza `RequestException` (timeout, error de conexión o código HTTP de error) o error de decodificación JSON, `fetch_cultural_spaces` invoca `load_fallback_csv` aplicando los mismos filtros de nombre, municipio, departamento y tipo de lugar.
- [x] La interfaz muestra un banner de advertencia (`alert-warning`) explicando que se están presentando datos reales de respaldo local y actualiza la etiqueta de fuente en el pie de página.
- [x] Verificado mediante la prueba automatizada `test_api_failure_falls_back_to_local_csv` en `cultural_spaces/tests.py`.
```

---

### HU-07 (Copiar y pegar como nuevo Issue en GitHub — Columna `Ready`)

**Add a title:**
```text
HU-07: Paginación de resultados ($offset y $limit) para explorar más de 40 espacios por consulta
```

**Add a description:**
```markdown
**Prioridad:** Medium  
**Responsable:** Andres  
**Estado en Project:** Ready (Priorizado para Sprint 2)

### Contexto y Propósito
Actualmente las consultas a `te39-v28f.json` traen los primeros 40 registros ordenados alfabéticamente (`$limit=40`). Para departamentos con alta concentración de espacios culturales (como Antioquia con 7.558 registros o Cundinamarca con 2.521), el usuario se beneficiará de controles de paginación (`Anterior` / `Siguiente`) basados en el parámetro `$offset` de Socrata.

### Historia de Usuario
> **Como** gestor cultural que consulta un departamento con cientos de espacios registrados,  
> **quiero** navegar entre páginas de resultados (`Anterior` y `Siguiente`) conservando mis filtros de búsqueda activos,  
> **para** explorar más allá de los primeros 40 espacios culturales sin sobrecargar el tiempo de carga inicial.

### Criterios de Aceptación
- [ ] La vista acepta el parámetro GET `page` (entero positivo, por defecto `1`) y calcula `$offset = (page - 1) * limit`.
- [ ] La plantilla muestra enlaces de navegación `Página anterior` y `Página siguiente` preservando los parámetros `q`, `municipio`, `departamento` y `tipo_lugar` en la URL.
- [ ] Si `page` recibe un valor no numérico o menor que 1, se normaliza a `1` sin provocar errores.
```

---

### HU-08 (Copiar y pegar como nuevo Issue en GitHub — Columna `Backlog`)

**Add a title:**
```text
HU-08: Autocompletado dinámico de municipios según el departamento seleccionado
```

**Add a description:**
```markdown
**Prioridad:** Low  
**Responsable:** Juliana  
**Estado en Project:** Backlog (Identificado en Retrospectiva para Sprint 2)

### Contexto y Propósito
Durante las pruebas y la retrospectiva del Sprint 1 se identificó que varios nombres de municipios en `datos.gov.co` contienen tildes o grafías específicas (ej. `"Curumaní"`, `"San José de Cúcuta"`, `"Chía"`). Proveer una lista de sugerencias (`<datalist>`) o selector dinámico de municipios al elegir un departamento reducirá errores de digitación del usuario.

### Historia de Usuario
> **Como** ciudadano que busca espacios culturales en un municipio cuyo nombre lleva tildes,  
> **quiero** contar con sugerencias de nombres de municipios válidos para el departamento elegido,  
> **para** seleccionar rápidamente mi municipio sin fallar en la búsqueda por diferencias ortográficas o de tildes.

### Criterios de Aceptación
- [ ] El servicio consulta o mantiene en caché la agregación Socrata `$select=departamento,municipio&$group=departamento,municipio`.
- [ ] El campo `municipio` del formulario ofrece sugerencias autocompletables (`<datalist>`) acordes con los municipios registrados en el dataset `te39-v28f`.
```
