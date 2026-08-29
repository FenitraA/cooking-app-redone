from django.db import models

from households.models import Household
from core.models import BaseModel, ImageCloudStorage


class UnitGroup(BaseModel):
    id_prefix = "unit_group"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
    symbol = models.CharField(
        max_length=128,
        unique=True,
    )


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
        UnitGroup,
        on_delete=models.CASCADE,
        related_name="ingredient_units",
    )


class IngredientType(BaseModel):
    id_prefix = "ingredient_type"

    name = models.CharField(
        max_length=128,
        unique=True,
    )


class Ingredient(BaseModel, ImageCloudStorage):
    id_prefix = "ingredient"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
    estimated_price = models.DecimalField(max_digits=16, decimal_places=2)
    ingredient_type = models.ForeignKey(
        IngredientType,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    ingredient_unit = models.ForeignKey(
        IngredientUnit,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )


class Seller(BaseModel):
    id_prefix = "seller"

    name = models.CharField(
        max_length=128,
        unique=True,
    )


class IngredientStock(BaseModel):
    id_prefix = "ingredient_stock"

    unit_cost = models.DecimalField(max_digits=16, decimal_places=2)
    quantity = models.DecimalField(max_digits=16, decimal_places=2)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_stocks",
    )
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name="ingredient_stocks",
    )
    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="ingredient_stocks",
    )
