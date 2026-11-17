"""Service layer for reading, cleaning, and filtering cultural spaces from datos.gov.co."""
from collections import Counter
import csv
from pathlib import Path
from typing import Any
import requests

DATASET_ID = "te39-v28f"
SOCRATA_ENDPOINT = f"https://www.datos.gov.co/resource/{DATASET_ID}.json"
DATASET_PORTAL_URL = (
    "https://www.datos.gov.co/Cultura/"
    "Espacios-de-las-Artes-las-Culturas-y-los-Saberes/te39-v28f"
)
PUBLISHER_ENTITY = "Ministerio de las Culturas, las Artes y los Saberes - MinCultura, Bogotá D.C."
DEFAULT_LIMIT = 40
MAX_LIMIT = 100
DEFAULT_TIMEOUT = 8
MAX_FILTER_LENGTH = 100
FALLBACK_CSV_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "cultural_spaces_sample.csv"
)

PLACEHOLDER_VALUES = {
    "",
    "sin dato",
    "sin información",
    "sin informacion",
    "no registra",
    "no aplica",
    "n/a",
    "na",
    "null",
    "none",
    "-",
}


def clamp_limit(limit: Any) -> int:
    """Ensure the requested record limit is an integer bounded between 1 and MAX_LIMIT."""
    try:
        parsed = int(limit)
    except (TypeError, ValueError):
        return DEFAULT_LIMIT
    return max(1, min(parsed, MAX_LIMIT))

SPACE_TYPE_CHOICES = [
    "Biblioteca",
    "Casa de Cultura",
    "Museo / Entidad Museal",
    "Escuela de música",
    "Escenario - LEP",
    "Archivo Histórico",
    "Bienes Inmuebles Patrimoniales - BICN",
    "Emisora comunitaria",
    "Emisora comercial",
    "Sitio Arqueológico",
]

DEPARTMENT_CHOICES = [
    "Amazonas",
    "Antioquia",
    "Arauca",
    "Atlántico",
    "Bogotá, D. C.",
    "Bolívar",
    "Boyacá",
    "Caldas",
    "Caquetá",
    "Casanare",
    "Cauca",
    "Cesar",
    "Chocó",
    "Córdoba",
    "Cundinamarca",
    "Guainía",
    "Guaviare",
    "Huila",
    "La Guajira",
    "Magdalena",
    "Meta",
    "Nariño",
    "Norte de Santander",
    "Putumayo",
    "Quindío",
    "Risaralda",
    "San Andrés y Providencia",
    "Santander",
    "Sucre",
    "Tolima",
    "Valle del Cauca",
    "Vaupés",
    "Vichada",
]


def _clean_field(raw_value: Any, default_text: str) -> str:
    """Return a trimmed string or default_text if the value is missing or placeholder."""
    if raw_value is None:
        return default_text
    text = str(raw_value).strip()
    if text.lower() in PLACEHOLDER_VALUES:
        return default_text
    return text


def sanitize_soql_value(raw_input: str | None) -> str:
    """Sanitize user input before embedding into a Socrata $where clause.

    Strips surrounding whitespace, removes control characters, caps length,
    and escapes single quotes (' -> '') to prevent SoQL syntax errors or injection.
    """
    if not raw_input:
        return ""
    cleaned = "".join(ch for ch in str(raw_input) if ch.isprintable()).strip()
    cleaned = cleaned[:MAX_FILTER_LENGTH]
    return cleaned.replace("'", "''")


def build_soql_where(
    query: str = "",
    municipality: str = "",
    department: str = "",
    space_type: str = "",
) -> str:
    """Construct a safe SoQL $where clause from user filter parameters."""
    clauses: list[str] = []

    safe_query = sanitize_soql_value(query)
    if safe_query:
        clauses.append(f"upper(nombre_del_lugar) like upper('%{safe_query}%')")

    safe_municipality = sanitize_soql_value(municipality)
    if safe_municipality:
        clauses.append(f"upper(municipio) like upper('%{safe_municipality}%')")

    safe_department = sanitize_soql_value(department)
    if safe_department:
        clauses.append(f"upper(departamento) = upper('{safe_department}')")

    safe_space_type = sanitize_soql_value(space_type)
    if safe_space_type:
        clauses.append(f"upper(tipo_lugar) = upper('{safe_space_type}')")

    return " AND ".join(clauses)


def normalize_space_record(raw_row: dict[str, Any]) -> dict[str, str]:
    """Normalize a raw Socrata or CSV record so incomplete data never breaks the UI."""
    if not isinstance(raw_row, dict):
        raw_row = {}
    return {
        "name": _clean_field(raw_row.get("nombre_del_lugar"), "Nombre no disponible"),
        "space_type": _clean_field(raw_row.get("tipo_lugar"), "Sin clasificar"),
        "department": _clean_field(raw_row.get("departamento"), "No especificado"),
        "municipality": _clean_field(raw_row.get("municipio"), "No especificado"),
        "address": _clean_field(raw_row.get("direcci_n_f_sica"), "No especificada"),
        "description": _clean_field(
            raw_row.get("descripci_n"), "Sin descripción disponible"
        ),
        "source": _clean_field(raw_row.get("fuente"), "No registrada"),
        "divipola": _clean_field(raw_row.get("divipola"), "N/D"),
    }


def summarize_spaces(items: list[dict[str, str]]) -> dict[str, Any]:
    """Compute a statistical summary over the current list of cultural spaces."""
    if not items:
        return {
            "total_count": 0,
            "unique_municipalities": 0,
            "unique_departments": 0,
            "top_types": [],
        }

    municipalities = {
        (item.get("department", ""), item.get("municipality", ""))
        for item in items
        if item.get("municipality") and item.get("municipality") != "No especificado"
    }
    departments = {
        item.get("department", "")
        for item in items
        if item.get("department") and item.get("department") != "No especificado"
    }
    type_counts = Counter(item.get("space_type", "Sin clasificar") for item in items)
    top_types = [
        {"name": stype, "count": count} for stype, count in type_counts.most_common(4)
    ]

    return {
        "total_count": len(items),
        "unique_municipalities": len(municipalities),
        "unique_departments": len(departments),
        "top_types": top_types,
    }


def _filter_fallback_records(
    records: list[dict[str, str]],
    query: str = "",
    municipality: str = "",
    department: str = "",
    space_type: str = "",
) -> list[dict[str, str]]:
    """Apply equivalent case-insensitive filters over local CSV records."""
    q_norm = (query or "").strip().lower()
    muni_norm = (municipality or "").strip().lower()
    dept_norm = (department or "").strip().lower()
    type_norm = (space_type or "").strip().lower()

    filtered: list[dict[str, str]] = []
    for item in records:
        if q_norm and q_norm not in item["name"].lower():
            continue
        if muni_norm and muni_norm not in item["municipality"].lower():
            continue
        if dept_norm and dept_norm != item["department"].lower():
            continue
        if type_norm and type_norm != item["space_type"].lower():
            continue
        filtered.append(item)
    # Same order as the API query ($order=nombre_del_lugar ASC).
    return sorted(filtered, key=lambda item: item["name"].upper())


def format_thousands(value: int) -> str:
    """Format an integer with dots as thousands separator (Colombian style): 29961 -> 29.961."""
    return f"{value:,}".replace(",", ".")


def _read_fallback_records(csv_path: Path = FALLBACK_CSV_PATH) -> list[dict[str, str]]:
    """Read and normalize every record stored in the local backup CSV file."""
    if not csv_path.exists():
        return []
    with csv_path.open(mode="r", encoding="utf-8") as csv_file:
        return [normalize_space_record(row) for row in csv.DictReader(csv_file)]


def count_fallback_records(csv_path: Path = FALLBACK_CSV_PATH) -> int:
    """Return how many records the local backup sample contains."""
    return len(_read_fallback_records(csv_path))


def load_fallback_csv(
    csv_path: Path = FALLBACK_CSV_PATH,
    limit: int = DEFAULT_LIMIT,
    query: str = "",
    municipality: str = "",
    department: str = "",
    space_type: str = "",
) -> list[dict[str, str]]:
    """Read real backup records from the local CSV file when the API is unreachable."""
    filtered = _filter_fallback_records(
        _read_fallback_records(csv_path),
        query=query,
        municipality=municipality,
        department=department,
        space_type=space_type,
    )
    return filtered[:limit]


MAX_GROUP_ROWS = 5000
MAX_PAGE = 10000


def parse_page(raw_page: Any) -> int:
    """Validate the `page` query parameter: an integer between 1 and MAX_PAGE, else 1."""
    try:
        page = int(str(raw_page).strip())
    except (TypeError, ValueError):
        return 1
    if page < 1 or page > MAX_PAGE:
        return 1
    return page


def total_pages_for(total: int | None, limit: int = DEFAULT_LIMIT) -> int | None:
    """Number of pages needed to list `total` records, or None if the total is unknown."""
    if total is None:
        return None
    return max(1, -(-total // limit))


def _socrata_get(params: dict[str, str]) -> Any:
    """Run one GET against the Socrata endpoint and return the decoded JSON."""
    response = requests.get(
        SOCRATA_ENDPOINT,
        params=params,
        timeout=DEFAULT_TIMEOUT,
        headers={"Accept": "application/json"},
    )
    response.raise_for_status()
    return response.json()


def fetch_total_count(where_clause: str = "") -> int | None:
    """Ask Socrata how many records match the filters, using $select=count(*).

    Returns None when the count cannot be obtained, so the interface can
    still show the listed records without a total.
    """
    params: dict[str, str] = {"$select": "count(*) AS total"}
    if where_clause:
        params["$where"] = where_clause
    try:
        payload = _socrata_get(params)
        return int(payload[0]["total"])
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        return None


def fetch_aggregate_summary(where_clause: str = "") -> dict[str, Any] | None:
    """Compute the summary over ALL records that match the filters, not only the listed page.

    Uses two grouped Socrata queries:
      1. $group=tipo_lugar -> total records and records per space type.
      2. $group=departamento, municipio -> distinct municipalities and departments.
    Returns None if any query fails, so the caller can fall back to the listed page.
    """
    type_params: dict[str, str] = {
        "$select": "tipo_lugar, count(*) AS total",
        "$group": "tipo_lugar",
        "$order": "total DESC",
        "$limit": str(MAX_GROUP_ROWS),
    }
    place_params: dict[str, str] = {
        "$select": "departamento, municipio",
        "$group": "departamento, municipio",
        "$limit": str(MAX_GROUP_ROWS),
    }
    if where_clause:
        type_params["$where"] = where_clause
        place_params["$where"] = where_clause

    try:
        type_rows = _socrata_get(type_params)
        place_rows = _socrata_get(place_params)
        if not isinstance(type_rows, list) or not isinstance(place_rows, list):
            return None

        type_counts: Counter[str] = Counter()
        for row in type_rows:
            space_type = _clean_field(row.get("tipo_lugar"), "Sin clasificar")
            type_counts[space_type] += int(row["total"])

        municipalities: set[tuple[str, str]] = set()
        departments: set[str] = set()
        for row in place_rows:
            department = _clean_field(row.get("departamento"), "No especificado")
            municipality = _clean_field(row.get("municipio"), "No especificado")
            if department != "No especificado":
                departments.add(department)
                if municipality != "No especificado":
                    municipalities.add((department, municipality))
    except (requests.RequestException, ValueError, KeyError, TypeError, AttributeError):
        return None

    return {
        "total_count": sum(type_counts.values()),
        "unique_municipalities": len(municipalities),
        "unique_departments": len(departments),
        "top_types": [
            {"name": name, "count": count} for name, count in type_counts.most_common(4)
        ],
    }


def fetch_cultural_spaces(
    query: str = "",
    municipality: str = "",
    department: str = "",
    space_type: str = "",
    limit: int = DEFAULT_LIMIT,
    page: int = 1,
) -> dict[str, Any]:
    """Fetch one page of cultural spaces from Socrata API with sanitized $where, timeout, and CSV fallback.

    Result keys:
      items: the requested page (at most `limit` records, alphabetical).
      page / offset: the page that was requested and its first record position (0-based).
      summary: indicators; summary_scope says whether they cover "all" matching
        records or only the "shown" page (when the aggregate queries fail).
      total_available: how many records match the filters (None if unknown).
    """
    safe_limit = clamp_limit(limit)
    safe_page = parse_page(page)
    offset = (safe_page - 1) * safe_limit
    where_clause = build_soql_where(
        query=query,
        municipality=municipality,
        department=department,
        space_type=space_type,
    )
    params: dict[str, str] = {
        "$limit": str(safe_limit),
        "$offset": str(offset),
        # :id breaks ties between equal names so pages never repeat or skip records.
        "$order": "nombre_del_lugar ASC, :id ASC",
    }
    if where_clause:
        params["$where"] = where_clause

    try:
        payload = _socrata_get(params)
        if not isinstance(payload, list):
            payload = []
        items = [normalize_space_record(item) for item in payload]

        if safe_page == 1 and len(items) < safe_limit:
            # The first page already contains every matching record.
            summary = summarize_spaces(items)
            summary_scope = "all"
            total_available: int | None = len(items)
        else:
            aggregate = fetch_aggregate_summary(where_clause)
            if aggregate is not None:
                summary = aggregate
                summary_scope = "all"
                total_available = aggregate["total_count"]
            else:
                summary = summarize_spaces(items)
                summary_scope = "shown"
                if 0 < len(items) < safe_limit:
                    # A short, non-empty page is the last one: the total is known.
                    total_available = offset + len(items)
                else:
                    total_available = fetch_total_count(where_clause)

        return {
            "items": items,
            "page": safe_page,
            "offset": offset,
            "limit": safe_limit,
            "summary": summary,
            "summary_scope": summary_scope,
            "total_available": total_available,
            "using_fallback": False,
            "sample_size": None,
            "error_message": None,
            "where_clause": where_clause,
            "source_label": "API Socrata en vivo (datos.gov.co)",
        }
    except (requests.RequestException, ValueError):
        all_records = _read_fallback_records()
        matching = _filter_fallback_records(
            all_records,
            query=query,
            municipality=municipality,
            department=department,
            space_type=space_type,
        )
        sample_size = len(all_records)
        return {
            "items": matching[offset:offset + safe_limit],
            "page": safe_page,
            "offset": offset,
            "limit": safe_limit,
            "summary": summarize_spaces(matching),
            "summary_scope": "all",
            "total_available": len(matching),
            "using_fallback": True,
            "sample_size": sample_size,
            "error_message": (
                "No fue posible conectar con la API de datos.gov.co en este momento. "
                f"Mostrando una muestra real de respaldo guardada localmente "
                f"({format_thousands(sample_size)} registros descargados de datos.gov.co, "
                "/data/cultural_spaces_sample.csv). No representa el conjunto completo: "
                "los totales e indicadores se calculan solo sobre esa muestra."
            ),
            "where_clause": where_clause,
            "source_label": "Muestra local CSV (/data/cultural_spaces_sample.csv - datos.gov.co)",
        }
