# Arquitectura de Requisitos: Catálogo Completo de 15 Historias de Usuario e Issues (HU-01 a HU-15)

Documento diseñado desde la perspectiva de **Arquitectura de Software** para el *Directorio Ciudadano de Espacios de las Artes, las Culturas y los Saberes de Colombia* (`te39-v28f` — `datos.gov.co`).

Al analizar el sistema capa por capa (**Ingesta y Resiliencia de Datos**, **Sanitización y Dominio**, **Búsqueda y Analítica**, **Experiencia de Usuario y Accesibilidad**, **Calidad/Seguridad DevSecOps** y **Evolución Arquitectónica**), el producto se descompone en **15 Historias de Usuario (HU-01 a HU-15)**:
* **11 Historias implementadas en el Sprint 1** (9 en `Done` y 2 en `In Review` asociadas al [Pull Request #4](https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4)).
* **4 Historias de evolución arquitectónica para el Sprint 2** (2 en `Ready` y 2 en `Backlog`).
* **Distribución equitativa en el equipo:** 5 HUs para `Andres`, 5 HUs para `Santiago` y 5 HUs para `Juliana`.

---

## 1. Matriz Arquitectónica de las 15 Historias de Usuario (Tablero GitHub Project)

| ID | Capa Arquitectónica | Título para GitHub Issue | Prioridad | Responsable | Módulo / Evidencia Técnica | Estado (`Status`) |
|---|---|---|---|---|---|---|
| **HU-01** *(Issue #1)* | 1. Ingesta Socrata | `HU-01: Consulta en tiempo real de espacios culturales desde la API Socrata de datos.gov.co` | `High` | `Andres` | `services.py` (`fetch_cultural_spaces`) | `Done` |
| **HU-02** *(Issue #2)* | 3. Búsqueda y Dominio | `HU-02: Búsqueda por palabra clave y filtrado multicriterio por departamento, municipio y tipo` | `High` | `Santiago` | `services.py` (`build_soql_where`) + `PR #4` | `In Review` |
| **HU-03** *(Issue #3)* | 3. Analítica en Memoria | `HU-03: Resumen estadístico dinámico de la oferta cultural en la consulta actual` | `Medium` | `Juliana` | `services.py` (`summarize_spaces`) | `Done` |
| **HU-04** | 2. Seguridad SoQL | `HU-04: Saneamiento de entradas contra inyección SoQL ($where) y acotamiento de $limit` | `High` | `Santiago` | `services.py` (`sanitize_soql_value`, `clamp_limit`) | `Done` |
| **HU-05** | 2. Limpieza de Datos | `HU-05: Normalización de registros con datos ausentes o comodines ("Sin Dato", "No registra")` | `High` | `Juliana` | `services.py` (`normalize_space_record`, `_clean_field`) + `PR #4` | `In Review` |
| **HU-06** | 1. Resiliencia / Fallback | `HU-06: Conmutación automática (Fallback) a CSV local real ante fallos o timeouts de red` | `High` | `Andres` | `services.py` (`load_fallback_csv`), `/data/cultural_spaces_sample.csv` | `Done` |
| **HU-09** | 1. Gobernanza de Datos | `HU-09: Trazabilidad de fuente activa (API en vivo vs CSV local) y atribución oficial MinCultura` | `Medium` | `Andres` | `views.py`, `index.html` (`source_label`, `publisher_entity`) | `Done` |
| **HU-10** | 4. Estados de Interfaz | `HU-10: Gestión diferenciada de búsqueda en blanco, estado vacío con detalle de filtros y restablecimiento` | `High` | `Santiago` | `views.py` (`empty_search_submitted`, `has_active_filters`), `index.html` | `Done` |
| **HU-11** | 4. UI/UX y Accesibilidad | `HU-11: Interfaz responsiva (CSS Grid) con semántica HTML5 y atributos de accesibilidad ARIA` | `Medium` | `Juliana` | `templates/cultural_spaces/index.html` (`role="status"`, `aria-label`) | `Done` |
| **HU-12** | 5. QA y Testing | `HU-12: Suite de pruebas automatizadas desacopladas con Mocks HTTP para casos críticos y bordes` | `High` | `Juliana` | `cultural_spaces/tests.py` (`SimpleTestCase`, 7 tests en `OK`) | `Done` |
| **HU-13** | 5. Arquitectura y Seguridad | `HU-13: Configuración Django sin estado (Stateless), protección de SECRET_KEY por entorno y .gitignore` | `Medium` | `Santiago` | `config/settings.py` (`DATABASES = {}`), `.gitignore`, `requirements.txt` | `Done` |
| **HU-07** | 6. Evolución (Sprint 2) | `HU-07: Paginación de resultados ($offset y $limit) para explorar más de 40 espacios por consulta` | `Medium` | `Andres` | Arquitectura de paginación SoQL | `Ready` |
| **HU-14** | 6. Evolución (Sprint 2) | `HU-14: Exportación ciudadana de los resultados filtrados actuales a formato CSV descargable` | `Medium` | `Santiago` | Endpoint de descarga `StreamingHttpResponse` | `Ready` |
| **HU-08** | 6. Evolución (Sprint 2) | `HU-08: Autocompletado dinámico y tolerancia a tildes en nombres de municipios por departamento` | `Low` | `Juliana` | Agregación `$group=departamento,municipio` + `<datalist>` | `Backlog` |
| **HU-15** | 6. Evolución (Sprint 2) | `HU-15: Integración de coordenadas geográficas (latitud/longitud) con enlace directo a mapa externo` | `Low` | `Andres` | Campos `latitud`, `longitud` y `coordenadas` de `te39-v28f` | `Backlog` |

---

## 2. Fichas Detalladas Listas para Copiar y Pegar en GitHub Issues (`HU-01` a `HU-15`)

---

### HU-01 — Capa de Ingesta Socrata *(Ya creada como Issue #1)*

**Add a title:**
```text
HU-01: Consulta en tiempo real de espacios culturales desde la API Socrata de datos.gov.co
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Ingesta de Datos Abiertos (Socrata API Client)  
**Prioridad:** High  
**Responsable:** Andres  
**Estado en Project:** Done

### Contexto Arquitectónico
La aplicación requiere consumir directamente la API Socrata del conjunto de datos oficial **Espacios de las Artes, las Culturas y los Saberes (`te39-v28f`)** sin duplicar los 29.961 registros en una base de datos relacional local. Las peticiones HTTP deben incluir control estricto de tiempo de espera (`timeout`) y ordenamiento alfabético determinista (`$order=nombre_del_lugar ASC`).

### Historia de Usuario
> **Como** ciudadano interesado en la oferta cultural de Colombia,  
> **quiero** consultar en tiempo real el listado de espacios culturales directamente desde `datos.gov.co`,  
> **para** visualizar información actualizada de bibliotecas, museos, casas de cultura y escenarios artísticos con su ubicación y descripción.

### Criterios de Aceptación
- [x] `fetch_cultural_spaces` realiza peticiones `GET` a `https://www.datos.gov.co/resource/te39-v28f.json` con `DEFAULT_TIMEOUT = 8` segundos y cabecera `Accept: application/json`.
- [x] Cada registro retornado expone en la plantilla: `name`, `space_type`, `municipality`, `department`, `address`, `description`, `source` y `divipola`.
- [x] Si el payload JSON devuelto por la API no es una lista válida, el servicio lo degrada de forma segura a `[]` sin lanzar excepciones en la vista.
```

---

### HU-02 — Capa de Búsqueda y Dominio *(Ya creada como Issue #2)*

**Add a title:**
```text
HU-02: Búsqueda por palabra clave y filtrado multicriterio por departamento, municipio y tipo
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Lógica de Dominio y Consulta SoQL  
**Prioridad:** High  
**Responsable:** Santiago  
**Estado en Project:** In Review (Refs PR #4)

### Contexto Arquitectónico
Para permitir consultas selectivas sobre 29.961 registros nacionales sin transferir todo el dataset al servidor Django, el filtrado debe delegarse al motor SoQL de Socrata mediante la cláusula `$where`, combinando condiciones de texto parcial (`like`) y coincidencia exacta (`=`) de forma insensible a mayúsculas/minúsculas (`upper(...)`).

### Historia de Usuario
> **Como** estudiante, investigador o gestor cultural,  
> **quiero** buscar espacios por palabra clave en el nombre y combinar filtros por departamento, municipio y tipo de espacio cultural,  
> **para** acotar la consulta únicamente a los lugares culturales relevantes de mi territorio de interés.

### Criterios de Aceptación
- [x] `build_soql_where` construye dinámicamente cláusulas `AND` para `nombre_del_lugar` (`like '%...%'`), `municipio` (`like '%...%'`), `departamento` (`=`) y `tipo_lugar` (`=`).
- [x] El formulario en `index.html` ofrece selectores poblados con los 32 departamentos + Bogotá D.C. (`DEPARTMENT_CHOICES`) y las 10 tipologías principales (`SPACE_TYPE_CHOICES`).
- [x] Los filtros equivalentes se aplican también en memoria (`_filter_fallback_records`) cuando opera el modo de contingencia CSV.
```

---

### HU-03 — Capa de Analítica en Memoria *(Ya creada como Issue #3)*

**Add a title:**
```text
HU-03: Resumen estadístico dinámico de la oferta cultural en la consulta actual
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Servicio de Agregación y Analítica Descriptiva  
**Prioridad:** Medium  
**Responsable:** Juliana  
**Estado en Project:** Done

### Contexto Arquitectónico
El usuario no solo necesita leer tarjetas individuales, sino también interpretar agregaciones inmediatas del subconjunto consultado (cardinalidad de resultados, dispersión municipal/departamental y distribución de frecuencias por categoría cultural).

### Historia de Usuario
> **Como** investigador cultural o ciudadano,  
> **quiero** observar un panel de indicadores estadísticos sobre los resultados de mi búsqueda actual,  
> **para** dimensionar de un vistazo cuántos espacios se muestran, cuántos municipios y departamentos abarcan y qué tipos de espacios predominan.

### Criterios de Aceptación
- [x] `summarize_spaces` utiliza `collections.Counter` y conjuntos (`set`) para calcular `total_count`, `unique_municipalities`, `unique_departments` y las 4 categorías más frecuentes (`top_types`).
- [x] Excluye del conteo territorial los valores por defecto `"No especificado"`.
- [x] Cuando la lista de entrada está vacía (`[]`), retorna contadores en `0` y `top_types: []` sin errores.
```

---

### HU-04 — Capa de Seguridad SoQL *(Copiar como nuevo Issue)*

**Add a title:**
```text
HU-04: Saneamiento de entradas contra inyección SoQL ($where) y acotamiento de $limit
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Seguridad de Aplicación y Validación de Entradas  
**Prioridad:** High  
**Responsable:** Santiago  
**Estado en Project:** Done

### Contexto Arquitectónico
La construcción de cláusulas `$where` mediante interpolación de cadenas requiere defensa explícita contra inyección SoQL y errores de sintaxis producidos por comillas simples (`'`), caracteres de control no imprimibles o cadenas excesivamente largas, así como validación de rangos para el parámetro `$limit`.

### Historia de Usuario
> **Como** responsable técnico y usuario de la plataforma,  
> **quiero** que todas las entradas de búsqueda sean saneadas y acotadas antes de enviarse a la API de `datos.gov.co`,  
> **para** prevenir inyecciones en la consulta SoQL (`' OR '1'='1`), fallos HTTP 400 por comillas simples (ej. `"O'Higgins"`) o sobrecargas por límites inválidos.

### Criterios de Aceptación
- [x] `sanitize_soql_value` filtra caracteres no imprimibles (`ch.isprintable()`), recorta espacios extremos, trunca a `MAX_FILTER_LENGTH = 100` y escapa cada comilla simple (`'` -> `''`).
- [x] `clamp_limit` garantiza que `$limit` sea siempre un entero dentro del rango `[1, 100]`, usando `DEFAULT_LIMIT = 40` ante entradas no numéricas.
- [x] Verificado con los tests unitarios `test_soql_where_sanitizes_single_quotes_and_injection` y `test_extended_placeholders_and_invalid_limit_are_handled_safely`.
```

---

### HU-05 — Capa de Limpieza y Normalización de Datos *(Copiar como nuevo Issue)*

**Add a title:**
```text
HU-05: Normalización de registros con datos ausentes o comodines ("Sin Dato", "No registra")
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Transformación y Calidad de Datos (Data Cleansing)  
**Prioridad:** High  
**Responsable:** Juliana  
**Estado en Project:** In Review (Refs PR #4)

### Contexto Arquitectónico
Los registros provenientes de múltiples fuentes del sector cultura (PULEP, RNBP, SIMCO, ICANH) presentan heterogeneidad: campos omitidos en el JSON, valores `None`, cadenas vacías o textos marcadores como `"Sin Dato"`, `"Sin información"`, `"No registra"`, `"No aplica"`, `"N/A"` o `"-"`.

### Historia de Usuario
> **Como** ciudadano que consulta fichas de espacios culturales,  
> **quiero** que cualquier dato faltante o marcador técnico sea reemplazado por un texto claro y uniforme en español,  
> **para** leer tarjetas completas y comprensibles sin que la interfaz se rompa ni muestre valores como `None`, `null` o `Sin Dato`.

### Criterios de Aceptación
- [x] `_clean_field` y `normalize_space_record` evalúan el conjunto `PLACEHOLDER_VALUES` (insensible a mayúsculas) y asignan textos semánticos por campo: `"Nombre no disponible"`, `"Sin clasificar"`, `"No especificado"`, `"No especificada"`, `"Sin descripción disponible"` y `"No registrada"`.
- [x] Si `normalize_space_record` recibe un objeto que no es diccionario, devuelve una estructura válida con todos los valores por defecto.
- [x] Verificado en `test_incomplete_record_does_not_break_interface` y `test_extended_placeholders_and_invalid_limit_are_handled_safely`.
```

---

### HU-06 — Capa de Resiliencia y Contingencia Offline *(Copiar como nuevo Issue)*

**Add a title:**
```text
HU-06: Conmutación automática (Fallback) a CSV local real ante fallos o timeouts de red
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Resiliencia e Integración de Datos (Fallback Pattern)  
**Prioridad:** High  
**Responsable:** Andres  
**Estado en Project:** Done

### Contexto Arquitectónico
Para garantizar alta disponibilidad durante demostraciones o caídas del portal `datos.gov.co`, el servicio implementa el patrón *Fallback*: ante cualquier `requests.RequestException` (timeout, DNS, conexión rechazada, HTTP 5xx/4xx) o JSON corrupto, conmuta de forma transparente a `/data/cultural_spaces_sample.csv`.

### Historia de Usuario
> **Como** usuario del directorio cultural,  
> **quiero** seguir consultando y filtrando espacios culturales reales desde un respaldo local cuando la API de `datos.gov.co` no esté disponible,  
> **para** no sufrir pantallas de error 500 y completar mi consulta aun sin conexión a internet.

### Criterios de Aceptación
- [x] El archivo `/data/cultural_spaces_sample.csv` contiene registros reales descargados del dataset `te39-v28f` con las mismas columnas oficiales.
- [x] `load_fallback_csv` lee el archivo con `csv.DictReader`, normaliza cada fila con `normalize_space_record` y aplica `_filter_fallback_records` respetando los filtros del usuario y el límite solicitado.
- [x] El diccionario de respuesta activa `using_fallback = True` y expone `error_message` para informar al usuario en pantalla.
- [x] Verificado con `test_api_failure_falls_back_to_local_csv`.
```

---

### HU-09 — Capa de Gobernanza y Transparencia de Datos *(Copiar como nuevo Issue)*

**Add a title:**
```text
HU-09: Trazabilidad de fuente activa (API en vivo vs CSV local) y atribución oficial MinCultura
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Gobernanza de Datos Abiertos y Transparencia  
**Prioridad:** Medium  
**Responsable:** Andres  
**Estado en Project:** Done

### Contexto Arquitectónico
El uso responsable de datos públicos exige mostrar en todo momento la entidad publicadora oficial verificada en los metadatos (`/api/views/te39-v28f.json`), el identificador del dataset (`te39-v28f`), el sistema de origen de cada registro (`fuente`: PULEP, SIMCO, RNBP, ICANH) y si los datos provienen en ese instante de la API en vivo o del archivo CSV de respaldo.

### Historia de Usuario
> **Como** ciudadano o evaluador,  
> **quiero** identificar claramente en la interfaz la entidad publicadora, el enlace oficial de `datos.gov.co`, el registro de origen de cada espacio y si la consulta actual provino de la API en vivo o del respaldo local,  
> **para** verificar la autenticidad y trazabilidad de los datos mostrados.

### Criterios de Aceptación
- [x] El encabezado y el pie de página muestran `Ministerio de las Culturas, las Artes y los Saberes - MinCultura, Bogotá D.C.`, el ID `te39-v28f` y enlaces clicables al portal y al endpoint JSON.
- [x] El pie de página informa dinámicamente `Fuente actual: API Socrata en vivo (datos.gov.co)` o `Fuente actual: Respaldo local CSV (/data/cultural_spaces_sample.csv - datos.gov.co)`.
- [x] Cada tarjeta individual muestra el campo `Registro origen` (`fuente`).
```

---

### HU-10 — Capa de Estados de Interfaz y Navegación *(Copiar como nuevo Issue)*

**Add a title:**
```text
HU-10: Gestión diferenciada de búsqueda en blanco, estado vacío con detalle de filtros y restablecimiento
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Controlador de Vista (`views.py`) y Estados de Presentación  
**Prioridad:** High  
**Responsable:** Santiago  
**Estado en Project:** Done

### Contexto Arquitectónico
La vista debe distinguir tres situaciones de interacción diferentes: (1) carga inicial sin parámetros GET, (2) envío explícito del formulario con todos los campos vacíos o con espacios en blanco (`empty_search_submitted`), y (3) búsqueda con filtros activos (`has_active_filters`) que retorna 0 coincidencias.

### Historia de Usuario
> **Como** usuario que interactúa con el formulario de búsqueda,  
> **quiero** recibir mensajes claros cuando envío el formulario en blanco o cuando ningún espacio coincide con mis filtros (viendo qué filtros apliqué y pudiendo limpiarlos en un clic),  
> **para** entender siempre por qué veo determinados resultados y cómo ajustar mi consulta.

### Criterios de Aceptación
- [x] Cuando `bool(request.GET)` es verdadero pero todos los campos tras `.strip()` están vacíos, `empty_search_submitted` es `True` y se muestra un banner azul informativo junto al listado general.
- [x] Cuando `spaces` está vacío, se muestra el estado vacío con el detalle de los filtros activos (`Nombre`, `Municipio`, `Departamento`, `Tipo`) y el botón `"Ver todos los espacios"`.
- [x] El botón `"Limpiar filtros"` redirige a `{% url 'cultural_spaces:index' %}` restableciendo todos los parámetros.
```

---

### HU-11 — Capa de UI/UX y Accesibilidad Ciudadana *(Copiar como nuevo Issue)*

**Add a title:**
```text
HU-11: Interfaz responsiva (CSS Grid) con semántica HTML5 y atributos de accesibilidad ARIA
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Presentación Frontend, Semántica Web y Accesibilidad  
**Prioridad:** Medium  
**Responsable:** Juliana  
**Estado en Project:** Done

### Contexto Arquitectónico
Una herramienta ciudadana de datos abiertos debe ser rápida, legible en pantallas móviles y de escritorio sin depender de frameworks externos pesados que puedan fallar por CDN, y debe respetar estándares de semántica HTML5 y accesibilidad web.

### Historia de Usuario
> **Como** ciudadano que accede desde computador o teléfono móvil (incluyendo usuarios de tecnologías de asistencia),  
> **quiero** una interfaz adaptable, con contraste adecuado, etiquetas asociadas a cada campo y regiones semánticas claras,  
> **para** navegar y filtrar el directorio cultural cómodamente desde cualquier dispositivo.

### Criterios de Aceptación
- [x] Uso de `CSS Grid` responsivo (`grid-template-columns: repeat(auto-fill, minmax(310px, 1fr))`) para las tarjetas de espacios y para el formulario/resumen.
- [x] Todos los `<input>` y `<select>` tienen su correspondiente `<label for="id_...">` explícito.
- [x] Las regiones de búsqueda, resumen y alertas utilizan etiquetas semánticas (`<header>`, `<main>`, `<section>`, `<article>`, `<footer>`) y atributos `aria-label` y `role="status"`.
```

---

### HU-12 — Capa de Aseguramiento de Calidad (QA & Testing) *(Copiar como nuevo Issue)*

**Add a title:**
```text
HU-12: Suite de pruebas automatizadas desacopladas con Mocks HTTP para casos críticos y bordes
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Aseguramiento de Calidad y Pruebas Automatizadas  
**Prioridad:** High  
**Responsable:** Juliana  
**Estado en Project:** Done

### Contexto Arquitectónico
Las pruebas automatizadas no deben depender de conexión en vivo a internet ni de una base de datos SQL para ejecutarse de manera determinista y rápida en cualquier entorno de integración. Se utiliza `django.test.SimpleTestCase` junto con `unittest.mock.patch("cultural_spaces.services.requests.get")`.

### Historia de Usuario
> **Como** desarrollador del equipo ágil,  
> **quiero** contar con una suite de pruebas automatizadas con mocks HTTP que verifique los casos obligatorios y de borde en milisegundos,  
> **para** comprobar antes de cada commit o Pull Request que ningún cambio rompa el recorrido funcional ni la seguridad SoQL.

### Criterios de Aceptación
- [x] `cultural_spaces/tests.py` implementa 7 pruebas automatizadas que cubren: (1) búsqueda normal y resumen, (2) cero coincidencias, (3) entrada vacía/espacios, (4) registros con campos `None`/`""`/`"Sin Dato"`, (5) placeholders extendidos y límite fuera de rango, (6) saneamiento de comillas simples e inyección SoQL, y (7) caída de red con fallback a CSV.
- [x] `python manage.py test -v 2` ejecuta las 7 pruebas en `< 0.05s` con resultado `OK` sin requerir base de datos.
```

---

### HU-13 — Capa de Arquitectura Stateless y DevSecOps *(Copiar como nuevo Issue)*

**Add a title:**
```text
HU-13: Configuración Django sin estado (Stateless), protección de SECRET_KEY por entorno y .gitignore
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Configuración de Infraestructura, Seguridad y Reproducibilidad  
**Prioridad:** Medium  
**Responsable:** Santiago  
**Estado en Project:** Done

### Contexto Arquitectónico
Siguiendo el principio de mínimo privilegio y arquitectura sin estado (*Stateless*), la aplicación prescinde de motor de base de datos (`DATABASES = {}`), evita almacenar claves o secretos de producción en el código fuente y fija las versiones exactas de todas sus dependencias en `requirements.txt`.

### Historia de Usuario
> **Como** evaluador o desarrollador que clona el repositorio,  
> **quiero** que el proyecto inicie sin requerir migraciones de base de datos ni archivos secretos ocultos, y que el repositorio esté libre de artefactos locales,  
> **para** instalar y ejecutar la aplicación en cualquier máquina siguiendo únicamente el `README.md`.

### Criterios de Aceptación
- [x] `config/settings.py` obtiene `SECRET_KEY` desde `os.environ.get("DJANGO_SECRET_KEY") or get_random_secret_key()` y define `DATABASES = {}`.
- [x] `.gitignore` excluye `.venv/`, `venv/`, `__pycache__/`, `*.pyc`, `db.sqlite3`, `.env` y `.idea/`.
- [x] `requirements.txt` contiene versiones exactas fijadas (`Django==6.1.3`, `requests==2.34.2`, etc.) y `python manage.py check` reporta `0 issues`.
```

---

### HU-07 — Capa de Evolución Arquitectónica (Sprint 2 — Columna `Ready`)

**Add a title:**
```text
HU-07: Paginación de resultados ($offset y $limit) para explorar más de 40 espacios por consulta
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Escalabilidad de Consultas Socrata (Sprint 2)  
**Prioridad:** Medium  
**Responsable:** Andres  
**Estado en Project:** Ready

### Contexto Arquitectónico
Actualmente las consultas a `te39-v28f.json` retornan un máximo de 40 registros por página (`DEFAULT_LIMIT = 40`). Para departamentos con miles de espacios culturales (ej. Antioquia con 7.558 registros), se requiere paginación basada en `$offset` y `$limit`.

### Historia de Usuario
> **Como** gestor cultural que consulta un departamento con cientos de espacios registrados,  
> **quiero** navegar entre páginas de resultados (`Anterior` y `Siguiente`) conservando mis filtros activos,  
> **para** explorar la totalidad de los espacios culturales más allá de los primeros 40 resultados.

### Criterios de Aceptación
- [ ] `views.py` lee el parámetro GET `page` (validado como entero `>= 1`) y calcula `offset = (page - 1) * limit`.
- [ ] `services.py` envía `$offset` a la API Socrata (y rebana `filtered[offset:offset + limit]` en el fallback CSV).
- [ ] `index.html` presenta controles de navegación `Página anterior` y `Página siguiente` manteniendo los filtros en el querystring.
```

---

### HU-14 — Capa de Evolución Arquitectónica (Sprint 2 — Columna `Ready`)

**Add a title:**
```text
HU-14: Exportación ciudadana de los resultados filtrados actuales a formato CSV descargable
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Interoperabilidad y Reutilización de Datos Abiertos (Sprint 2)  
**Prioridad:** Medium  
**Responsable:** Santiago  
**Estado en Project:** Ready

### Contexto Arquitectónico
Investigadores, docentes y periodistas de datos que filtran un subconjunto de espacios culturales (por ejemplo, todas las bibliotecas de un departamento) suelen necesitar descargar esa tabla limpia en formato CSV para trabajarla en hojas de cálculo.

### Historia de Usuario
> **Como** investigador o periodista cultural,  
> **quiero** descargar en un archivo CSV los espacios culturales resultantes de mi búsqueda actual,  
> **para** analizarlos o compartirlos fuera de línea conservando la atribución oficial de `datos.gov.co`.

### Criterios de Aceptación
- [ ] Nueva ruta `/exportar-csv/` en `cultural_spaces/urls.py` que reutiliza `fetch_cultural_spaces` con los mismos parámetros de filtro activos.
- [ ] Retorna un `HttpResponse` con `Content-Type: text/csv; charset=utf-8` y encabezados normalizados en español.
```

---

### HU-08 — Capa de Evolución Arquitectónica (Sprint 2 — Columna `Backlog`)

**Add a title:**
```text
HU-08: Autocompletado dinámico y tolerancia a tildes en nombres de municipios por departamento
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Usabilidad de Búsqueda y Caché de Catálogos (Sprint 2)  
**Prioridad:** Low  
**Responsable:** Juliana  
**Estado en Project:** Backlog

### Contexto Arquitectónico
Identificado en la retrospectiva del Sprint 1: en Socrata los nombres de municipios contienen tildes (ej. `"Medellín"`, `"Curumaní"`, `"Chía"`). Proveer un `<datalist>` alimentado por una agregación ligera en caché reducirá búsquedas sin coincidencias por omisión de tildes.

### Historia de Usuario
> **Como** ciudadano que busca espacios culturales en un municipio cuyo nombre lleva tilde,  
> **quiero** recibir sugerencias autocompletables de municipios válidos al escribir en el formulario,  
> **para** seleccionar el nombre exacto registrado en `datos.gov.co` sin errores ortográficos.

### Criterios de Aceptación
- [ ] Servicio auxiliar que consulta `$select=departamento,municipio&$group=departamento,municipio` y almacena el catálogo en caché de memoria.
- [ ] El campo `municipio` en `index.html` se vincula a un `<datalist>` con los municipios oficiales.
```

---

### HU-15 — Capa de Evolución Arquitectónica (Sprint 2 — Columna `Backlog`)

**Add a title:**
```text
HU-15: Integración de coordenadas geográficas (latitud/longitud) con enlace directo a mapa externo
```

**Add a description:**
```markdown
**Capa Arquitectónica:** Georreferenciación Ligera de Espacios Culturales (Sprint 2)  
**Prioridad:** Low  
**Responsable:** Andres  
**Estado en Project:** Backlog

### Contexto Arquitectónico
El dataset `te39-v28f` incluye las columnas `latitud`, `longitud` y `coordenadas` (`Point`). Sin introducir mapas complejos fuera del alcance mínimo, cada tarjeta que posea coordenadas válidas puede ofrecer un enlace externo directo (`Ver ubicación en mapa`) hacia OpenStreetMap.

### Historia de Usuario
> **Como** ciudadano o turista que desea visitar un espacio cultural,  
> **quiero** abrir la ubicación geográfica del lugar en un mapa externo cuando el registro cuente con coordenadas válidas,  
> **para** ubicar el escenario cultural incluso cuando su dirección física rural o arqueológica no sea estándar.

### Criterios de Aceptación
- [ ] `normalize_space_record` valida si `latitud` y `longitud` son números flotantes dentro del rango geográfico de Colombia.
- [ ] Si las coordenadas son válidas, la tarjeta en `index.html` muestra un enlace `"Ver en OpenStreetMap"` (`https://www.openstreetmap.org/?mlat=...&mlon=...`).
```
