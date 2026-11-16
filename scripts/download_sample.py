"""Download a representative offline sample of dataset te39-v28f from datos.gov.co.

The sample takes the same number of records from every space type
(tipo_lugar), so the offline fallback can answer searches for any type.
It keeps the original CSV columns published by the portal.

Usage (from the project root, with internet access):
    python scripts/download_sample.py
    python scripts/download_sample.py --per-type 30

The current sample file is only replaced if every download succeeds.
"""
import argparse
import csv
import io
import sys
from pathlib import Path

import requests

DATASET_ID = "te39-v28f"
JSON_ENDPOINT = f"https://www.datos.gov.co/resource/{DATASET_ID}.json"
CSV_ENDPOINT = f"https://www.datos.gov.co/resource/{DATASET_ID}.csv"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "cultural_spaces_sample.csv"
TIMEOUT = 30


def get_space_types() -> list[tuple[str, int]]:
    """Return every tipo_lugar in the dataset with its record count."""
    response = requests.get(
        JSON_ENDPOINT,
        params={
            "$select": "tipo_lugar, count(*) AS total",
            "$group": "tipo_lugar",
            "$order": "total DESC",
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return [
        (row["tipo_lugar"], int(row["total"]))
        for row in response.json()
        if row.get("tipo_lugar")
    ]


def get_rows_for_type(space_type: str, per_type: int) -> tuple[list[str], list[list[str]]]:
    """Download up to per_type records of one space type in the original CSV format."""
    safe_type = space_type.replace("'", "''")
    response = requests.get(
        CSV_ENDPOINT,
        params={
            "$where": f"tipo_lugar = '{safe_type}'",
            "$limit": str(per_type),
            "$order": ":id",
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    response.encoding = "utf-8"
    rows = list(csv.reader(io.StringIO(response.text)))
    if not rows:
        return [], []
    return rows[0], rows[1:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--per-type", type=int, default=20, help="records per space type (default 20)")
    args = parser.parse_args()

    try:
        space_types = get_space_types()
        header: list[str] = []
        all_rows: list[list[str]] = []
        for space_type, total in space_types:
            type_header, rows = get_rows_for_type(space_type, args.per_type)
            if type_header and not header:
                header = type_header
            all_rows.extend(rows)
            print(f"{space_type}: {len(rows)} de {total} registros")
    except (requests.RequestException, ValueError, KeyError) as error:
        print(f"No se pudo descargar la muestra; el archivo actual no se modificó. Detalle: {error}")
        return 1

    if not header or not all_rows:
        print("La API no devolvió registros; el archivo actual no se modificó.")
        return 1

    temp_path = OUTPUT_PATH.with_suffix(".tmp")
    with temp_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(all_rows)
    temp_path.replace(OUTPUT_PATH)

    print(f"Muestra guardada en {OUTPUT_PATH}: {len(all_rows)} registros de {len(space_types)} tipos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
