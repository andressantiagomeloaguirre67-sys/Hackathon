"""Views for browsing and filtering cultural spaces from datos.gov.co."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from . import services


def index(request: HttpRequest) -> HttpResponse:
    """Render the cultural spaces directory with search and filter controls."""
    raw_query = request.GET.get("q", "")
    raw_municipality = request.GET.get("municipio", "")
    raw_department = request.GET.get("departamento", "")
    raw_space_type = request.GET.get("tipo_lugar", "")

    query = raw_query.strip()
    municipality = raw_municipality.strip()
    department = raw_department.strip()
    space_type = raw_space_type.strip()

    has_active_filters = any([query, municipality, department, space_type])
    empty_search_submitted = bool(request.GET) and not has_active_filters

    result = services.fetch_cultural_spaces(
        query=query,
        municipality=municipality,
        department=department,
        space_type=space_type,
    )

    context = {
        "spaces": result["items"],
        "using_fallback": result["using_fallback"],
        "error_message": result["error_message"],
        "source_label": result["source_label"],
        "filters": {
            "q": query,
            "municipio": municipality,
            "departamento": department,
            "tipo_lugar": space_type,
        },
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
