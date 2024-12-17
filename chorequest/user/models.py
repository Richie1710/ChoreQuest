from django.contrib.auth.models import AbstractUser
from django.db import models

class UserAccount(AbstractUser):
    """Custom user model for Chore Quest.

    This model represents the player account.
    """
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.username