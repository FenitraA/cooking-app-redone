from django.db import models

from core.models import BaseModel


class ItemCategory(BaseModel):
    id_prefix = "item_category"

    name = models.CharField(
        max_length=128,
        unique=True,
    )

    # internal and stable identifier
    code = models.CharField(
        max_length=128,
        unique=True,
    )
