from django.contrib import admin

from .models import Shopping, ItemCategory, ShoppingItem, ItemToBuy

admin.site.register(Shopping)
admin.site.register(ItemCategory)
admin.site.register(ShoppingItem)
admin.site.register(ItemToBuy)
