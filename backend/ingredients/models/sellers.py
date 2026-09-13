from django.db import models

from core.models import BaseModel


class Seller(BaseModel):
    id_prefix = "seller"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
