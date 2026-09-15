from django.db import models


class HouseholdQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)