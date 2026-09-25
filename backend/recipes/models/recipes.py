from django.db import models

from core.models import BaseModelPlusImageCloudStorage
from django.core.validators import MinLengthValidator
from core.validators import validate_positive
from recipes.querysets.recipes import RecipeQuerySet


class Recipe(BaseModelPlusImageCloudStorage):
    id_prefix = "recipe"

    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(2),
        ],
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    estimated_time = models.IntegerField(
        validators=[
            validate_positive,
        ],
    )

    parallel_cooking = models.IntegerField(
        validators=[
            validate_positive,
        ],
    )

    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="recipes",
    )

    objects = RecipeQuerySet.as_manager()