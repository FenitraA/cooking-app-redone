from django.db import models

from core.models import BaseModel


class IngredientType(BaseModel):
    id_prefix = "ingredient_type"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
