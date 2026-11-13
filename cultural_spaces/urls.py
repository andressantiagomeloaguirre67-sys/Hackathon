"""URL routes for the cultural_spaces application."""
from django.urls import path
from . import views

app_name = "cultural_spaces"

urlpatterns = [
    path("", views.index, name="index"),
]
