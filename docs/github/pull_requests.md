# Pull Request Abierto en GitHub

* **Pull Request #4:** https://github.com/andressantiagomeloaguirre67-sys/Hackathon/pull/4
* **Rama origen:** `feature/improve-empty-states` → **Rama destino:** `main`
* **Estado:** `Open` — Pendiente de revisión y fusión (NO fusionado en `main`).
* **Referencia:** `Refs #2` (https://github.com/andressantiagomeloaguirre67-sys/Hackathon/issues/2)

---

## Título del Pull Request
`Mejorar manejo de respuestas vacías, placeholders extendidos y límite seguro en consultas Socrata (Refs #2)`

## Cuerpo del Pull Request

### Resumen
Este cambio mejora la resiliencia de `cultural_spaces/services.py`, `cultural_spaces/templates/cultural_spaces/index.html` y `cultural_spaces/tests.py`:
1. **Validación de límite (`clamp_limit`) y marcadores de posición extendidos:** Garantiza que el parámetro `limit` enviado a Socrata (`$limit`) esté siempre acotado entre `1` y `100` aunque se invoque con valores fuera de rango (`0`, negativos o excesivos), y amplía `PLACEHOLDER_VALUES` para cubrir textos reales como `"sin información"`, `"sin informacion"`, `"no registra"` y `"no aplica"`.
2. **Retroalimentación detallada en estado vacío (`index.html`):** Cuando una búsqueda no arroja coincidencias, el bloque de estado vacío muestra explícitamente qué filtros activos (`q`, `municipio`, `departamento`, `tipo_lugar`) produjeron cero resultados.
3. **Nuevas pruebas automatizadas (`tests.py`):** Añade `test_extended_placeholders_and_invalid_limit_are_handled_safely` y verifica que el estado sin coincidencias muestre el término buscado.

### Por qué se realizó
Durante la revisión del manejo de errores y datos incompletos se detectó que algunos registros gubernamentales emplean `"Sin información"` o `"No registra"` en lugar de `"Sin Dato"`, y que el usuario se beneficia de ver exactamente qué filtro activo produjo 0 coincidencias antes de limpiar su búsqueda.

### Cómo se verificó
* **Antes del cambio (`python manage.py test -v 2`):** `Ran 6 tests in 0.019s — OK`.
* **Después del cambio (`python manage.py test -v 2`):** `Ran 7 tests — OK`.

### Estado
Este Pull Request queda **abierto y pendiente de revisión** por un compañero antes de fusionarse a `main`.

`Refs #2`
