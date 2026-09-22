from decimal import Decimal

from django.db import models
from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    Prefetch,
    Sum,
    Value,
)
from django.db.models.functions import Coalesce

from recipes.models import RecipeIngredient


class PlanningRecipeQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)

    def with_related(self):
        return (
            self.select_related(
                "recipe",
                "household",
            )
            .prefetch_related(
                Prefetch(
                    "recipe__recipe_ingredients",
                    queryset=RecipeIngredient.objects
                    .active()
                    .with_related()
                )
            )
        )

    def with_estimated_cost_price(self):
        return self.annotate(
            estimated_cost_price=ExpressionWrapper(
                Coalesce(
                    Sum(
                        F(
                            "recipe__recipe_ingredients__quantity"
                        )
                        * F(
                            "recipe__recipe_ingredients__ingredient__estimated_price"
                        )
                    ),
                    Value(Decimal("0.00")),
                )
                * F("nb_serving"),
                output_field=DecimalField(
                    max_digits=16,
                    decimal_places=2,
                ),
            )
        )
    def filter_start_date(self, start_date=None):
        if start_date is not None:
            return self.filter(planning_date__gte=start_date)
        return self

    def filter_end_date(self, end_date=None):
        if end_date is not None:
            return self.filter(planning_date__lte=end_date)
        return self