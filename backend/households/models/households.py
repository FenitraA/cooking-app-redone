from django.db import models
from django.core.validators import MinLengthValidator
from core.models import BaseModel
from households.querysets import HouseholdQuerySet

class Household(BaseModel):
    id_prefix = "household"
    
    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[MinLengthValidator(2)],
    )
    objects = HouseholdQuerySet.as_manager()
