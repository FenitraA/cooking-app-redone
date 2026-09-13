from django.db import models

from core.models import BaseModel


class ShoppingItem(BaseModel):
    id_prefix = "shopping_item"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
    description = models.TextField(null=True)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    units_bought = models.DecimalField(max_digits=16, decimal_places=2)

    ingredient = models.ForeignKey(
        "ingredients.Ingredient",
        null=True,
        on_delete=models.SET_NULL,
        related_name="shopping_items",
    )
    shopping = models.ForeignKey(
        "shoppings.Shopping",
        on_delete=models.CASCADE,
        related_name="shopping_items",
    )
    item_category = models.ForeignKey(
        "shoppings.ItemCategory",
        on_delete=models.CASCADE,
        related_name="shopping_items",
    )
