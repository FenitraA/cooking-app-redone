from django.db import models
from django.core.validators import MinLengthValidator
from core.models import BaseModel
from ingredients.querysets.sellers import SellerQuerySet


class Seller(BaseModel):
    id_prefix = "seller"

    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            MinLengthValidator(2),
        ],
    )
    
    objects = SellerQuerySet.as_manager()
