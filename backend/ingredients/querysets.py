from django.db.models import (
    F,
    DecimalField,
    ExpressionWrapper,
    OuterRef,
    Subquery,
    Sum,
    Value,
)
from django.db.models.functions import Coalesce
from django.db import models
from django.apps import apps



class IngredientQuerySet(models.QuerySet):

    def active(self):
        return self.filter(state__gt=0)
    
    def with_related(self):
        return self.select_related(
            "ingredient_type",
            "ingredient_unit",
            "ingredient_unit__unit_group",
        )
        
    def with_quantity_left(self):
        IngredientStock = apps.get_model('ingredients', 'IngredientStock')
        MealIngredient = apps.get_model('recipes', 'MealIngredient')

        # ----------------------------------------
        # Quantity used from each stock
        # ----------------------------------------

        used_quantity_subquery = (
            MealIngredient.objects.filter(
                ingredient_stock=OuterRef("pk"),
                state__gt=0,
                meal__state__gt=0,
            )
            .values("ingredient_stock")
            .annotate(total=Sum("quantity"))
            .values("total")
        )

        # ----------------------------------------
        # Quantity remaining for each ingredient
        # ----------------------------------------

        quantity_left_subquery = (
            IngredientStock.objects.filter(
                ingredient=OuterRef("pk"),
                state__gt=0,
            )
            .annotate(
                used_quantity=Coalesce(
                    Subquery(
                        used_quantity_subquery,
                        output_field=DecimalField(
                            max_digits=16,
                            decimal_places=2,
                        ),
                    ),
                    Value(
                        0,
                        output_field=DecimalField(
                            max_digits=16,
                            decimal_places=2,
                        ),
                    ),
                ),
            )
            .annotate(
                total_left=ExpressionWrapper(
                    F("quantity") - F("used_quantity"),
                    output_field=DecimalField(
                        max_digits=16,
                        decimal_places=2,
                    ),
                ),
            )
            .values("ingredient")
            .annotate(quantity_left=Sum("total_left"))
            .values("quantity_left")
        )

        return self.annotate(
            quantity_left=Coalesce(
                Subquery(
                    quantity_left_subquery,
                    output_field=DecimalField(
                        max_digits=16,
                        decimal_places=2,
                    ),
                ),
                Value(
                    0,
                    output_field=DecimalField(
                        max_digits=16,
                        decimal_places=2,
                    ),
                ),
            ),
        )

    def filter_name(self, name=None):
        if name:
            return self.filter(name__icontains=name)
        return self

    def filter_type(self, type_id=None):
        if type_id:
            return self.filter(ingredient_type_id=type_id)
        return self

    def filter_stock(self, min_stock=None):
        if min_stock is not None:
            return self.filter(quantity_left__gte=min_stock)
        return self

    def apply_sorting(self, sort_by, sort_direction):
        sort_direction = (sort_direction or "asc").lower()
        if sort_by == "unit_cost":
            self = self.annotate(
                unit_cost=ExpressionWrapper(
                    F("estimated_price")
                    / Coalesce(
                        F("ingredient_unit__multiplier_to_base"),
                        Value(1),
                    ),
                    output_field=DecimalField(
                        max_digits=16,
                        decimal_places=2,
                    ),
                )
            )
            sort_field = "-unit_cost" if sort_direction == "desc" else "unit_cost"
            return self.order_by(
                "ingredient_unit__unit_group_id",
                sort_field,
                "name",
            )
        elif sort_by == "quantity_left":
            sort_field = (
                "-quantity_left" if sort_direction == "desc" else "quantity_left"
            )
            return self.order_by(
                "ingredient_unit__unit_group_id",
                sort_field,
                "name",
            )
        else:
            return self.order_by(
                "ingredient_unit__unit_group_id",
                "name",
            )
