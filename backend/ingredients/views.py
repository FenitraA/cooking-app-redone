from django.db.models import F, DecimalField, ExpressionWrapper
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets
from ingredients.models import (
    Ingredient,
    IngredientStock,
    IngredientType,
    IngredientUnit,
    Seller,
    UnitGroup,
)
from ingredients.serializers import (
    IngredientSerializer,
    IngredientStockSerializer,
    IngredientTypeSerializer,
    IngredientUnitSerializer,
    SellerSerializer,
    UnitGroupSerializer,
)


@extend_schema_view(
    list=extend_schema(tags=["UnitGroups"]),
    retrieve=extend_schema(tags=["UnitGroups"]),
    create=extend_schema(tags=["UnitGroups"]),
    update=extend_schema(tags=["UnitGroups"]),
    partial_update=extend_schema(tags=["UnitGroups"]),
    destroy=extend_schema(tags=["UnitGroups"]),
)
class UnitGroupViewSet(viewsets.ModelViewSet):
    queryset = UnitGroup.objects.all()
    serializer_class = UnitGroupSerializer
    permission_classes = [DjangoModelPermissions]


@extend_schema_view(
    list=extend_schema(tags=["IngredientUnits"]),
    retrieve=extend_schema(tags=["IngredientUnits"]),
    create=extend_schema(tags=["IngredientUnits"]),
    update=extend_schema(tags=["IngredientUnits"]),
    partial_update=extend_schema(tags=["IngredientUnits"]),
    destroy=extend_schema(tags=["IngredientUnits"]),
)
class IngredientUnitViewSet(viewsets.ModelViewSet):
    queryset = IngredientUnit.objects.all()
    serializer_class = IngredientUnitSerializer
    permission_classes = [DjangoModelPermissions]


@extend_schema_view(
    list=extend_schema(tags=["IngredientTypes"]),
    retrieve=extend_schema(tags=["IngredientTypes"]),
    create=extend_schema(tags=["IngredientTypes"]),
    update=extend_schema(tags=["IngredientTypes"]),
    partial_update=extend_schema(tags=["IngredientTypes"]),
    destroy=extend_schema(tags=["IngredientTypes"]),
)
class IngredientTypeViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientTypeSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Ingredient.objects.select_related(
            "ingredient_unit", "ingredient_type", "ingredient_unit__unit_group"
        ).filter(state__gt=0)

        # Query params
        name = self.request.query_params.get("name")
        type_id = self.request.query_params.get("type_id")
        min_stock = self.request.query_params.get("min_stock")
        sort_by = self.request.query_params.get("sort_by")
        sort_direction = self.request.query_params.get("sort_direction", "asc")

        # Filters
        if name:
            queryset = queryset.filter(name__icontains=name)

        if type_id:
            queryset = queryset.filter(ingredient_type_id=type_id)

        if min_stock:
            queryset = queryset.filter(quantity_left__gte=min_stock)

        # Sorting
        if sort_by == "unit_cost":
            queryset = queryset.annotate(
                unit_cost=ExpressionWrapper(
                    F("estimated_price") / F("ingredient_unit__multiplier_to_base"),
                    output_field=DecimalField(),
                )
            )

            order = "-unit_cost" if sort_direction == "desc" else "unit_cost"

            queryset = queryset.order_by(
                "ingredient_unit__unit_group_id", order, "name"
            )

        else:
            queryset = queryset.order_by("ingredient_unit__unit_group_id", "name")

        return queryset


@extend_schema_view(
    list=extend_schema(tags=["Ingredients"]),
    retrieve=extend_schema(tags=["Ingredients"]),
    create=extend_schema(tags=["Ingredients"]),
    update=extend_schema(tags=["Ingredients"]),
    partial_update=extend_schema(tags=["Ingredients"]),
    destroy=extend_schema(tags=["Ingredients"]),
)
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [DjangoModelPermissions]


@extend_schema_view(
    list=extend_schema(tags=["Sellers"]),
    retrieve=extend_schema(tags=["Sellers"]),
    create=extend_schema(tags=["Sellers"]),
    update=extend_schema(tags=["Sellers"]),
    partial_update=extend_schema(tags=["Sellers"]),
    destroy=extend_schema(tags=["Sellers"]),
)
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [DjangoModelPermissions]


@extend_schema_view(
    list=extend_schema(tags=["IngredientStocks"]),
    retrieve=extend_schema(tags=["IngredientStocks"]),
    create=extend_schema(tags=["IngredientStocks"]),
    update=extend_schema(tags=["IngredientStocks"]),
    partial_update=extend_schema(tags=["IngredientStocks"]),
    destroy=extend_schema(tags=["IngredientStocks"]),
)
class IngredientStockViewSet(viewsets.ModelViewSet):
    queryset = IngredientStock.objects.all()
    serializer_class = IngredientStockSerializer
    permission_classes = [DjangoModelPermissions]
