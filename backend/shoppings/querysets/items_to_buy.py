from django.db import models

class ItemToBuyQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)
    
    def with_related(self):
        return self.select_related(
            "item_category",
            "ingredient",
        )
    
    def filter_name(self, name=None):
        if name:
            return self.filter(name__icontains=name)
        return self

    def filter_ingredient(self, ingredient_id=None):
        if ingredient_id is not None:
            return self.filter(ingredient_id=ingredient_id)
        return self