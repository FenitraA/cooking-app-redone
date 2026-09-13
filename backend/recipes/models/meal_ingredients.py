

from django.db import models

from core.models import TimestampedAndStated


class MealIngredient(TimestampedAndStated):
    id_prefix = "meal_ingredient"

    pk = models.CompositePrimaryKey("meal","ingredient_stock")
    
    quantity = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
    ingredient_unit = models.ForeignKey(
        "ingredients.IngredientUnit",
        on_delete=models.SET_NULL,
        null=True,
        related_name="meal_ingredients",
    )
    meal = models.ForeignKey(
        "recipes.Meal",
        on_delete=models.CASCADE,
        related_name="meal_ingredients",
    )
    ingredient_stock = models.ForeignKey(
        "ingredients.IngredientStock",
        on_delete=models.CASCADE,
        related_name="meal_ingredients",
    )