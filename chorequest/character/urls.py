"""URL configuration for the character app."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CharacterViewSet

# Router für ViewSets erstellen
router = DefaultRouter()
router.register(r"characters", CharacterViewSet)

# URLs für die API registrieren
urlpatterns = [
    path("api/", include(router.urls)),  # Fügt die URLs des Routers hinzu
]
