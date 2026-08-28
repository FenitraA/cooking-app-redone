from django.db import models

from backend.core.models import BaseModel, TimestampedAndStated

class MealIngredient(TimestampedAndStated):
    id_prefix = "meal_ingredient"
    
class Meal(BaseModel):
    id_prefix = "meal"
    
    
class RecipeIngredient(TimestampedAndStated):
    id_prefix = "recipe_ingredient"

class Recipe(BaseModel):
    id_prefix = "recipe"