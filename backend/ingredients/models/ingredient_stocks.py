from django.db import models

from core.models import BaseModel


class IngredientStock(BaseModel):
    id_prefix = "ingredient_stock"

    unit_cost = models.DecimalField(max_digits=16, decimal_places=2)
    quantity = models.DecimalField(max_digits=16, decimal_places=2)
    ingredient = models.ForeignKey(
        "ingredients.Ingredient",
        on_delete=models.CASCADE,
        related_name="ingredient_stocks",
    )
    seller = models.ForeignKey(
        "ingredients.Seller",
        on_delete=models.CASCADE,
        related_name="ingredient_stocks",
    )
    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="ingredient_stocks",
    )
