
from django.db import models

from core.models import TimestampedAndStated


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
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )

    ingredient = models.ForeignKey(
        "ingredients.Ingredient",
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )