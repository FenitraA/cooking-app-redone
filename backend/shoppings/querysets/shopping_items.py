from django.db import models

class ShoppingItemQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)
    
    def with_related_for_shopping(self):
            return self.select_related(
                "item_category",
                "ingredient"
            )
    def with_related(self):
        return self.select_related(
            "item_category",
            "ingredient",
            "shopping"
        )
    
    def filter_name(self, name=None):
        if name:
            return self.filter(name__icontains=name)
        return self

    def filter_ingredient(self, ingredient_id=None):
        if ingredient_id is not None:
            return self.filter(ingredient_id=ingredient_id)
        return self
    
    def filter_start_date(self, start_date=None):
        if start_date is not None:
            return self.filter(shopping__shopping_date__gte=start_date)
        return self

    def filter_end_date(self, end_date=None):
        if end_date is not None:
            return self.filter(shopping__shopping_date__lte=end_date)
        return self
