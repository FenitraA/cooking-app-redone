from django.apps import apps
from django.db import models
from django.db.models import Prefetch

class RecipeQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)

    def with_related(self):
        # Prefetch object import to avoid circular imports
        MealIngredient = apps.get_model(
            "recipes",
            "MealIngredient",
        )
        return (
            self.select_related(
                "recipe",
            )
            .prefetch_related(
                Prefetch(
                    "meal_ingredients",
                    queryset=MealIngredient.objects
                    .active()
                    .with_related()
                )
            )
        )