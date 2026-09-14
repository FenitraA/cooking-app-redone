    
from django.db import models

from core.models import BaseModel
from core.validators import validate_positive

class Meal(BaseModel):
    id_prefix = "meal"

    nb_serving = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[
            validate_positive,
        ],
    )

    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="meals",
    )
