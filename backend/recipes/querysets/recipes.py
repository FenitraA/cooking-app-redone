from django.db import models
from django.db.models import Prefetch

from recipes.models import MealIngredient


class RecipeQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)

    def with_related(self):
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