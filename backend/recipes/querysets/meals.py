from django.apps import apps
from django.db import models
from django.db.models import Prefetch

class MealQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)

    def with_related(self):
        # Prefetch object import to avoid circular imports
        RecipeIngredient = apps.get_model(
            "recipes",
            "RecipeIngredient",
        )
        return (
            self.select_related(
                "household",
            )
            .prefetch_related(
                Prefetch(
                    "recipe_ingredients",
                    queryset=RecipeIngredient.objects
                    .active()
                    .with_related()
                )
            )
        )