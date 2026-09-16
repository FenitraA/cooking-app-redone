

from django.db import models

from django.core.validators import MinLengthValidator
from core.models import BaseModel
from core.validators import validate_positive
from ingredients.querysets.ingredient_units import IngredientUnitQuerySet


class IngredientUnit(BaseModel):
    id_prefix = "ingredient_unit"

    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(2),
        ],
    )

    symbol = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(1),
        ],
    )

    multiplier_to_base = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[
            validate_positive,
        ],
    )

    unit_group = models.ForeignKey(
        "ingredients.UnitGroup",
        on_delete=models.CASCADE,
        related_name="ingredient_units",
    )

    objects = IngredientUnitQuerySet.as_manager()