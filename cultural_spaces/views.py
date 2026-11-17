"""Views for browsing, filtering, summarizing, and paginating cultural spaces from datos.gov.co."""
from urllib.parse import urlencode

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from . import services


def read_filters(request: HttpRequest) -> dict[str, str]:
    """Read the search filters from the query string, trimmed of surrounding spaces."""
    return {
        "q": request.GET.get("q", "").strip(),
        "municipio": request.GET.get("municipio", "").strip(),
        "departamento": request.GET.get("departamento", "").strip(),
        "tipo_lugar": request.GET.get("tipo_lugar", "").strip(),
    }


def filters_querystring(filters: dict[str, str]) -> str:
    """Encode only the active filters, so links (pages, downloads) keep the current search."""
    return urlencode({key: value for key, value in filters.items() if value})


def index(request: HttpRequest) -> HttpResponse:
    """Render the cultural spaces directory with search, filter, summary, and pagination controls."""
    filters = read_filters(request)
    has_active_filters = any(filters.values())
    submitted_keys = set(request.GET.keys()) - {"page"}
    empty_search_submitted = bool(submitted_keys) and not has_active_filters

    result = services.fetch_cultural_spaces(
        query=filters["q"],
        municipality=filters["municipio"],
        department=filters["departamento"],
        space_type=filters["tipo_lugar"],
        page=services.parse_page(request.GET.get("page", 1)),
    )

    items = result["items"]
    page = result["page"]
    total_available = result["total_available"]
    total_pages = services.total_pages_for(total_available, result["limit"])
    first_position = result["offset"] + 1
    last_position = result["offset"] + len(items)
    if total_pages is not None:
        has_next_page = page < total_pages
    else:
        has_next_page = len(items) == result["limit"]
    page_out_of_range = page > 1 and not items

    context = {
        "spaces": items,
        "summary": result["summary"],
        "top_types": [
            {"name": item["name"], "count": services.format_thousands(item["count"])}
            for item in result["summary"]["top_types"]
        ],
        "municipalities_display": services.format_thousands(
            result["summary"]["unique_municipalities"]
        ),
        "summary_covers_all": result["summary_scope"] == "all",
        "shown_count": len(items),
        "total_available": total_available,
        "total_available_display": (
            services.format_thousands(total_available)
            if total_available is not None
            else None
        ),
        "shows_partial_results": (
            total_available is not None and total_available > len(items) and bool(items)
        ),
        "page": page,
        "total_pages": total_pages,
        "total_pages_display": (
            services.format_thousands(total_pages) if total_pages is not None else None
        ),
        "first_position": services.format_thousands(first_position),
        "last_position": services.format_thousands(last_position),
        "has_previous_page": page > 1 and not page_out_of_range,
        "previous_page": page - 1,
        "has_next_page": has_next_page and not page_out_of_range,
        "next_page": page + 1,
        "page_out_of_range": page_out_of_range,
        "filters_query": filters_querystring(filters),
        "export_max_display": services.format_thousands(services.EXPORT_MAX_RECORDS),
        "export_is_truncated": (
            total_available is not None and total_available > services.EXPORT_MAX_RECORDS
        ),
        "using_fallback": result["using_fallback"],
        "sample_size": result["sample_size"],
        "error_message": result["error_message"],
        "source_label": result["source_label"],
        "filters": filters,
        "has_active_filters": has_active_filters,
        "empty_search_submitted": empty_search_submitted,
        "department_choices": services.DEPARTMENT_CHOICES,
        "space_type_choices": services.SPACE_TYPE_CHOICES,
        "dataset_id": services.DATASET_ID,
        "dataset_portal_url": services.DATASET_PORTAL_URL,
        "socrata_endpoint": services.SOCRATA_ENDPOINT,
        "publisher_entity": services.PUBLISHER_ENTITY,
    }
    return render(request, "cultural_spaces/index.html", context)


def export_csv(request: HttpRequest) -> HttpResponse:
    """Download the spaces that match the current filters as a CSV file (up to EXPORT_MAX_RECORDS)."""
    filters = read_filters(request)
    result = services.fetch_spaces_for_export(
        query=filters["q"],
        municipality=filters["municipio"],
        department=filters["departamento"],
        space_type=filters["tipo_lugar"],
    )
    # The BOM (\ufeff) lets Excel on Windows open the file with accents intact.
    content = "\ufeff" + services.build_spaces_csv(result["items"], result["source_label"])
    response = HttpResponse(content, content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{services.EXPORT_FILENAME}"'
    return response
