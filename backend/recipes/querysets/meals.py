from django.db import models
from django.db.models import Prefetch

from recipes.models import RecipeIngredient


class MealQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)

    def with_related(self):
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