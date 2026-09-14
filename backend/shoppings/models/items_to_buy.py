from django.db import models

from core.models import BaseModel
from django.core.validators import MinLengthValidator
from core.validators import validate_non_negative,validate_positive


class ItemToBuy(BaseModel):
    id_prefix = "item_to_buy"

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

    estimated_unit_price = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[
            validate_non_negative,
        ],
    )

    units_to_buy = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[
            validate_positive,
        ],
    )

    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="items_to_buy",
    )

    ingredient = models.ForeignKey(
        "ingredients.Ingredient",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="items_to_buy",
    )

    shopping_item = models.ForeignKey(
        "shoppings.ShoppingItem",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="items_to_buy",
    )

    item_category = models.ForeignKey(
        "shoppings.ItemCategory",
        on_delete=models.CASCADE,
        related_name="items_to_buy",
    )