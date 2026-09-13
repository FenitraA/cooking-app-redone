

from django.db import models

from core.models import BaseModel


class IngredientUnit(BaseModel):
    id_prefix = "ingredient_unit"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
    symbol = models.CharField(
        max_length=128,
        unique=True,
    )
    multiplier_to_base = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
    unit_group = models.ForeignKey(
        "ingredients.UnitGroup",
        on_delete=models.CASCADE,
        related_name="ingredient_units",
    )
