from django.db import models

from core.models import BaseModel

class Household(BaseModel):
    id_prefix = "household"
    
    name = models.CharField(
        max_length=128,
        unique=True,
    )
