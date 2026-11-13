"""Service layer for reading, cleaning, and filtering cultural spaces from datos.gov.co."""
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
PUBLISHER_ENTITY = "Ministerio de las Culturas, las Artes y los Saberes (MinCultura)"
DEFAULT_LIMIT = 40
DEFAULT_TIMEOUT = 8
MAX_FILTER_LENGTH = 100
FALLBACK_CSV_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "cultural_spaces_sample.csv"
)

PLACEHOLDER_VALUES = {"", "sin dato", "n/a", "na", "null", "none", "-"}

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
    return filtered


def load_fallback_csv(
    csv_path: Path = FALLBACK_CSV_PATH,
    limit: int = DEFAULT_LIMIT,
    query: str = "",
    municipality: str = "",
    department: str = "",
    space_type: str = "",
) -> list[dict[str, str]]:
    """Read real backup records from the local CSV file when the API is unreachable."""
    if not csv_path.exists():
        return []
    records: list[dict[str, str]] = []
    with csv_path.open(mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            records.append(normalize_space_record(row))
    filtered = _filter_fallback_records(
        records,
        query=query,
        municipality=municipality,
        department=department,
        space_type=space_type,
    )
    return filtered[:limit]


def fetch_cultural_spaces(
    query: str = "",
    municipality: str = "",
    department: str = "",
    space_type: str = "",
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    """Fetch cultural spaces from Socrata API with sanitized $where, timeout, and CSV fallback."""
    where_clause = build_soql_where(
        query=query,
        municipality=municipality,
        department=department,
        space_type=space_type,
    )
    params: dict[str, str] = {
        "$limit": str(limit),
        "$order": "nombre_del_lugar ASC",
    }
    if where_clause:
        params["$where"] = where_clause

    try:
        response = requests.get(
            SOCRATA_ENDPOINT,
            params=params,
            timeout=DEFAULT_TIMEOUT,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            payload = []
        items = [normalize_space_record(item) for item in payload]
        return {
            "items": items,
            "using_fallback": False,
            "error_message": None,
            "where_clause": where_clause,
            "source_label": "API Socrata en vivo (datos.gov.co)",
        }
    except (requests.RequestException, ValueError):
        fallback_items = load_fallback_csv(
            limit=limit,
            query=query,
            municipality=municipality,
            department=department,
            space_type=space_type,
        )
        return {
            "items": fallback_items,
            "using_fallback": True,
            "error_message": (
                "No fue posible conectar con la API de datos.gov.co en este momento. "
                "Mostrando datos reales de respaldo almacenados localmente (/data/cultural_spaces_sample.csv)."
            ),
            "where_clause": where_clause,
            "source_label": "Respaldo local CSV (/data/cultural_spaces_sample.csv - datos.gov.co)",
        }
