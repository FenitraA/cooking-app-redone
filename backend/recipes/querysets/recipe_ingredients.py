from django.db import models


class RecipeIngredientQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)

    def with_related(self):
        return self.select_related(
            "ingredient",
            "ingredient__ingredient_unit",
        )
