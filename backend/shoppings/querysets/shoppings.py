from django.db import models
from django.db.models import Prefetch

from shoppings.models.shopping_items import ShoppingItem


class ShoppingQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)

    def with_related(self):
        return self.prefetch_related(
            Prefetch(
                "shopping_items",
                queryset=ShoppingItem.objects.active().with_related_for_shopping(),
            )
        )

    def filter_start_date(self, start_date=None):
        if start_date is not None:
            return self.filter(shopping__shopping_date__gte=start_date)
        return self

    def filter_end_date(self, end_date=None):
        if end_date is not None:
            return self.filter(shopping__shopping_date__lte=end_date)
        return self
