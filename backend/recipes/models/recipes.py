from django.db import models

from core.models import BaseModelPlusImageCloudStorage


class Recipe(BaseModelPlusImageCloudStorage):
    id_prefix = "recipe"
    
    name = models.CharField(
        max_length=128,
        unique=True,
    )
    description = models.TextField(null=True)
    estimated_time = models.IntegerField()
    parallel_cooking = models.IntegerField()
    
    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
