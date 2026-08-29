from django.db import models

from core.models import BaseModel
from households.models import Household
from recipes.models import Recipe


class PlanningRecipe(BaseModel):
    id_prefix = "planning_recipe"

    nb_serving = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )

    planning_date = models.DateField()
    description = models.TextField(null=True)
    
    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="planning_recipes"
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="planning_recipes"
    )