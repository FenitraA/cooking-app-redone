from django.db import models
from django.contrib.auth.models import AbstractUser

from households.models import Household
from core.models import BaseModel

class AppUser(AbstractUser, BaseModel):
    id_prefix = "app_user"
    
    default_language = models.CharField(
        max_length=3,
        null=True,
        blank=True,
    )
    household = models.ForeignKey(
        Household,
        null=True,
        on_delete=models.CASCADE,
        related_name="users",
    )
    