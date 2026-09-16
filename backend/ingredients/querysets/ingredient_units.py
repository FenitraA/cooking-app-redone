from django.db import models

class IngredientUnitQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)
    
    def filter_name(self, name=None):
        if name:
            return self.filter(name__icontains=name)
        return self
