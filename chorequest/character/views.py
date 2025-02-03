"""Module contains the views for managing characters in the ChoreQuest application."""

from typing import ClassVar

from django.db.models.query import QuerySet
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Character
from .serializers import CharacterSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    """ViewSet für das Verwalten von Charakteren."""

    queryset = Character.objects.all()
    permission_classes: ClassVar[list] = [IsAuthenticated]
    serializer_class = CharacterSerializer

    def perform_create(self, serializer: CharacterSerializer) -> None:
        """Handle the creation of a new character."""
        # Überprüfen, ob der Benutzer im Request vorhanden ist
        user = self.request.user
        if user.is_authenticated:
            # Benutzer zuweisen
            serializer.save(user=user)
        else:
            msg = "User is not authenticated."
            raise serializers.ValidationError(msg)

    def get_queryset(self) -> QuerySet:
        """Gib nur die Charaktere des aktuellen Benutzers zurück."""
        return Character.objects.filter(user=self.request.user)
