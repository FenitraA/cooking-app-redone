from django.db import models
from django.core.validators import MinLengthValidator
from core.models import BaseModel


class UnitGroup(BaseModel):
    id_prefix = "unit_group"

    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(2),
        ],
    )

    symbol = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(1),
        ],
    )