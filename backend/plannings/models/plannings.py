from django.db import models

from core.models import BaseModel
from plannings.querysets.plannings import PlanningRecipeQuerySet
from recipes.models import Recipe
from core.validators import validate_positive

class PlanningRecipe(BaseModel):
    id_prefix = "planning_recipe"

    nb_serving = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[
            validate_positive,
        ],
    )

    planning_date = models.DateField()

    description = models.TextField(
        null=True,
        blank=True,
    )

    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="planning_recipes",
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="planning_recipes",
    )

    objects = PlanningRecipeQuerySet.as_manager()