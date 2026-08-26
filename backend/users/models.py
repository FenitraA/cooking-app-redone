from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

prefix = "user"

def generate_user_id():
    return f"{prefix}_{uuid.uuid4()}"

class AppUser(AbstractUser):
    id = models.CharField(
    max_length=64,
    primary_key=True,
    default=generate_user_id,
)
    default_language = models.CharField(
        max_length=3,
        null=True,
        blank=True,
    )

    state = models.IntegerField(
        default=1
    )
    
    