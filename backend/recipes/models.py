from django.db import models

from core.models import BaseModel, ImageCloudStorage, TimestampedAndStated
from households.models import Household
from ingredients.models import Ingredient, IngredientStock, IngredientUnit

class Recipe(BaseModel,ImageCloudStorage):
    id_prefix = "recipe"
    
    name = models.CharField(
        max_length=128,
        unique=True,
    )
    description = models.TextField(null=True)
    estimated_time = models.IntegerField()
    parallel_cooking = models.IntegerField()
    
    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    
class Meal(BaseModel):
    id_prefix = "meal"

    nb_serving = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="meals",
    )


class MealIngredient(TimestampedAndStated):
    id_prefix = "meal_ingredient"

    pk = models.CompositePrimaryKey("meal","ingredient_stock")
    
    quantity = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
    ingredient_unit = models.ForeignKey(
        IngredientUnit,
        on_delete=models.SET_NULL,
        null=True,
        related_name="meal_ingredients",
    )
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name="meal_ingredients",
    )
    ingredient_stock = models.ForeignKey(
        IngredientStock,
        on_delete=models.CASCADE,
        related_name="meal_ingredients",
    )

class RecipeIngredient(TimestampedAndStated):
    id_prefix = "recipe_ingredient"
    
    pk = models.CompositePrimaryKey("insertion_id","recipe","ingredient")

    quantity = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
    
    insertion_id = models.CharField(
        max_length=64,
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )