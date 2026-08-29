from django.db import models

from core.models import BaseModel
from households.models import Household
from ingredients.models import Ingredient


class ItemCategory(BaseModel):
    id_prefix = "item_category"

    name = models.CharField(
        max_length=128,
        unique=True,
    )

    # internal and stable identifier
    code = models.CharField(
        max_length=128,
        unique=True,
    )

class Shopping(BaseModel):
    id_prefix = "shopping"

    shopping_date = models.DateField()
    description = models.TextField(null=True)

    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="shoppings",
    )


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
        Ingredient,
        null=True,
        on_delete=models.SET_NULL,
        related_name="shopping_items",
    )
    shopping = models.ForeignKey(
        Shopping,
        on_delete=models.CASCADE,
        related_name="shopping_items",
    )
    item_category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        related_name="shopping_items",
    )


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
        Household,
        on_delete=models.CASCADE,
        related_name="items_to_buy",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        null=True,
        on_delete=models.SET_NULL,
        related_name="items_to_buy",
    )
    shopping_item = models.ForeignKey(
        ShoppingItem,
        null=True,
        on_delete=models.SET_NULL,
        related_name="items_to_buy",
    )
    item_category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        related_name="items_to_buy",
    )