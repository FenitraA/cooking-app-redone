from django.db import models

from core.models import BaseModel
from django.core.validators import MinLengthValidator

from shoppings.querysets.item_categories import ItemCategoryQuerySet


class ItemCategory(BaseModel):
    id_prefix = "item_category"

    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(2),
        ],
    )

    code = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(1),
        ],
    )
    
    objects = ItemCategoryQuerySet.as_manager()