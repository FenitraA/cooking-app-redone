from django.db import models
from django.core.validators import MinLengthValidator
from core.models import BaseModel


class IngredientType(BaseModel):
    id_prefix = "ingredient_type"

    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(2),
        ],
    )