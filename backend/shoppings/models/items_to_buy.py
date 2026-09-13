from django.db import models

from core.models import BaseModel


class ItemToBuy(BaseModel):
    id_prefix = "item_to_buy"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
    description = models.TextField(null=True)
    estimated_unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    units_to_buy = models.DecimalField(max_digits=16, decimal_places=2)

    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="items_to_buy",
    )
    ingredient = models.ForeignKey(
        "ingredients.Ingredient",
        null=True,
        on_delete=models.SET_NULL,
        related_name="items_to_buy",
    )
    shopping_item = models.ForeignKey(
        "shoppings.ShoppingItem",
        null=True,
        on_delete=models.SET_NULL,
        related_name="items_to_buy",
    )
    item_category = models.ForeignKey(
        "shoppings.ItemCategory",
        on_delete=models.CASCADE,
        related_name="items_to_buy",
    )
