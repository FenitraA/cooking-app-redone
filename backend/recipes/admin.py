from django.contrib import admin

from .models import Recipe, Meal

admin.site.register(Recipe)
admin.site.register(Meal)
