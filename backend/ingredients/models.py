from django.db import models

from backend.households.models import Household
from core.models import BaseModel

class Ingredient(BaseModel):
    id_prefix = "ingredient"

class Seller(BaseModel):
    id_prefix = "seller"
    
class IngredientStock(BaseModel):
    id_prefix = "ingredient_stock"
    
    unit_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2
    )
    quantity = models.DecimalField(
        max_digits=16,
        decimal_places=2
    )
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

class IngredientType(BaseModel):
    id_prefix = "ingredient_type"
    
class IngredientUnit(BaseModel):
    id_prefix = "ingredient_unit"
    
    
class UnitGroup(BaseModel):
    id_prefix = "unit_group"