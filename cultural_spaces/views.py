"""Views for browsing cultural spaces from datos.gov.co."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from . import services


def index(request: HttpRequest) -> HttpResponse:
    """Render the main cultural spaces directory page."""
    result = services.fetch_cultural_spaces()
    context = {
        "spaces": result["items"],
        "using_fallback": result["using_fallback"],
        "error_message": result["error_message"],
        "source_label": result["source_label"],
        "dataset_id": services.DATASET_ID,
        "dataset_portal_url": services.DATASET_PORTAL_URL,
        "socrata_endpoint": services.SOCRATA_ENDPOINT,
        "publisher_entity": services.PUBLISHER_ENTITY,
    }
    return render(request, "cultural_spaces/index.html", context)
