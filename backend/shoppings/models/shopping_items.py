from django.db import models

from core.models import BaseModel
from django.core.validators import MinLengthValidator
from core.validators import validate_non_negative, validate_positive
from shoppings.querysets.shopping_items import ShoppingItemQuerySet


class ShoppingItem(BaseModel):
    id_prefix = "shopping_item"

    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(2),
        ],
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    unit_price = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[
            validate_non_negative,
        ],
    )

    units_bought = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[
            validate_positive,
        ],
    )

    ingredient = models.ForeignKey(
        "ingredients.Ingredient",
        null=True,
        blank=True,
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

    objects = ShoppingItemQuerySet.as_manager()