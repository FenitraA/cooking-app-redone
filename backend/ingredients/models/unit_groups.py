from django.db import models

from core.models import BaseModel


class UnitGroup(BaseModel):
    id_prefix = "unit_group"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
    symbol = models.CharField(
        max_length=128,
        unique=True,
    )
