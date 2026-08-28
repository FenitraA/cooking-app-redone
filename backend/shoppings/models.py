from django.db import models

from backend.core.models import BaseModel
    
class ItemCategory(BaseModel):
    id_prefix = "item_category"

class ItemToBuy(BaseModel):
    id_prefix = "item_to_buy"
    
class ShoppingItem(BaseModel):
    id_prefix = "shopping_item"

class Shopping(BaseModel):
    id_prefix = "shopping"