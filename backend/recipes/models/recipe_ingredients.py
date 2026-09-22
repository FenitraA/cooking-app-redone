
from django.db import models

from django.core.validators import MinLengthValidator
from core.models import TimestampedAndStated
from core.validators import validate_positive
from recipes.querysets.recipe_ingredients import RecipeIngredientQuerySet


class RecipeIngredient(TimestampedAndStated):
    id_prefix = "recipe_ingredient"

    pk = models.CompositePrimaryKey(
        "insertion_id",
        "recipe",
        "ingredient",
    )

    quantity = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[
            validate_positive,
        ],
    )

    insertion_id = models.CharField(
        max_length=64,
        validators=[
            MinLengthValidator(1),
        ],
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

    objects = RecipeIngredientQuerySet.as_manager()