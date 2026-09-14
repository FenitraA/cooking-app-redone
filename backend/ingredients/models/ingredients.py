from decimal import Decimal

from django.db import models

from core.models import BaseModelPlusImageCloudStorage
from ingredients.querysets import IngredientQuerySet
from django.core.validators import MinLengthValidator
from core.validators import validate_non_negative


class Ingredient(BaseModelPlusImageCloudStorage):
    id_prefix = "ingredient"

    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[MinLengthValidator(2)],
    )
    estimated_price = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[validate_non_negative],
    )
    ingredient_type = models.ForeignKey(
        "ingredients.IngredientType",
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    ingredient_unit = models.ForeignKey(
        "ingredients.IngredientUnit",
        on_delete=models.CASCADE,
        related_name="ingredients",
    )

    objects = IngredientQuerySet.as_manager()
