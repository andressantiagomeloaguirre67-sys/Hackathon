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
FALLBACK_CSV_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "cultural_spaces_sample.csv"
)

PLACEHOLDER_VALUES = {"", "sin dato", "n/a", "na", "null", "none", "-"}


def _clean_field(raw_value: Any, default_text: str) -> str:
    """Return a trimmed string or default_text if the value is missing or placeholder."""
    if raw_value is None:
        return default_text
    text = str(raw_value).strip()
    if text.lower() in PLACEHOLDER_VALUES:
        return default_text
    return text


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


def load_fallback_csv(
    csv_path: Path = FALLBACK_CSV_PATH, limit: int = DEFAULT_LIMIT
) -> list[dict[str, str]]:
    """Read real backup records from the local CSV file when the API is unreachable."""
    if not csv_path.exists():
        return []
    records: list[dict[str, str]] = []
    with csv_path.open(mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            records.append(normalize_space_record(row))
            if len(records) >= limit:
                break
    return records


def fetch_cultural_spaces(limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
    """Fetch cultural spaces from Socrata API with timeout and CSV fallback."""
    params = {
        "$limit": str(limit),
        "$order": "nombre_del_lugar ASC",
    }
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
            "source_label": "API Socrata en vivo (datos.gov.co)",
        }
    except (requests.RequestException, ValueError):
        fallback_items = load_fallback_csv(limit=limit)
        return {
            "items": fallback_items,
            "using_fallback": True,
            "error_message": (
                "No fue posible conectar con la API de datos.gov.co en este momento. "
                "Mostrando datos reales de respaldo almacenados localmente (/data/cultural_spaces_sample.csv)."
            ),
            "source_label": "Respaldo local CSV (/data/cultural_spaces_sample.csv - datos.gov.co)",
        }
