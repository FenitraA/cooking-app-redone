from django.db import models


class IngredientStockQuerySet(models.QuerySet):
    def active(self):
        return self.filter(state__gt=0)

    def filter_ingredient(self, ingredient_id=None):
        if ingredient_id is not None:
            return self.filter(ingredient_id=ingredient_id)

        return self