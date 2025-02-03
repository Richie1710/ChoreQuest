"""Module contains tests for the UserAccount model."""

import pytest
from django.contrib.auth import get_user_model

UserAccount = get_user_model()

@pytest.mark.django_db
def test_useraccount_str_representation() -> None:
    """Test the string representation of the UserAccount model."""
    # Benutzer erstellen
    user = UserAccount.objects.create(username="unique_testuser84", email="testuser84@example.com")

    # Erwarteter String ist der Benutzername
    assert str(user) == "unique_testuser84"
