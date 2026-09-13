    
from django.db import models

from core.models import BaseModel


class Meal(BaseModel):
    id_prefix = "meal"

    nb_serving = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="meals",
    )

