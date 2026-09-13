from django.db import models

from core.models import BaseModel


class Shopping(BaseModel):
    id_prefix = "shopping"

    shopping_date = models.DateField()
    description = models.TextField(null=True)

    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="shoppings",
    )
