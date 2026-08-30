from django.contrib import admin

from .models import (
    Ingredient,
    IngredientUnit,
    IngredientStock,
    IngredientType,
    UnitGroup,
    Seller,
)

admin.site.register(Ingredient)
admin.site.register(IngredientUnit)
admin.site.register(IngredientStock)
admin.site.register(IngredientType)
admin.site.register(UnitGroup)
admin.site.register(Seller)
