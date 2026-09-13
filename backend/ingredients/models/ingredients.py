from django.db import models

from core.models import BaseModelPlusImageCloudStorage
from ingredients.querysets import IngredientQuerySet


class Ingredient(BaseModelPlusImageCloudStorage):
    id_prefix = "ingredient"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
    estimated_price = models.DecimalField(max_digits=16, decimal_places=2)
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

    # Query set manager
    objects = IngredientQuerySet.as_manager()
