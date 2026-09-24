from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from plannings.models import PlanningRecipe
from recipes.dataclasses import RecipeIngredientRead
from recipes.models import Recipe

@dataclass
class PlanningRecipeRead:
    planning_recipe: PlanningRecipe
    recipe: Recipe
    estimated_cost_price: Decimal
    recipe_ingredients: list[RecipeIngredientRead]

@dataclass
class PlanningRepartition:
    planning_group_date : date
    day_name : str
    planning_recipes : list[PlanningRecipeRead]
    estimated_cost_price : Decimal