from dataclasses import dataclass
from decimal import Decimal

@dataclass
class RecipeIngredientBase:
    insertion_id: str | None
    ref_ingredient_id: str | None
    ref_recipe_id: str
    quantity: Decimal


@dataclass
class RecipeIngredientRead:
    recipe_ingredient_base: RecipeIngredientBase
    recipe_name: str
    ingredient_name: str
    ingredient_unit: str
    estimated_cost_per_unit: Decimal

