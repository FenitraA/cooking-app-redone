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

from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    OuterRef,
    Subquery,
    Sum,
    Value,
)
from django.db.models.functions import Coalesce

from ingredients.serializers import (
    IngredientSearchSerializer,
    IngredientSerializer,
    IngredientStockSerializer,
    IngredientTypeSerializer,
    IngredientUnitSerializer,
    SellerSerializer,
    UnitGroupSerializer,
)
from recipes.models import MealIngredient


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
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer
    permission_classes = [DjangoModelPermissions]


@extend_schema_view(
    list=extend_schema(tags=["Ingredients"],parameters=[IngredientSearchSerializer]),
    retrieve=extend_schema(tags=["Ingredients"]),
    create=extend_schema(tags=["Ingredients"]),
    update=extend_schema(tags=["Ingredients"]),
    partial_update=extend_schema(tags=["Ingredients"]),
    destroy=extend_schema(tags=["Ingredients"]),
)
class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return (
            Ingredient.objects.active()
            .with_related()
            .with_quantity_left()
            .filter_name(self.request.query_params.get("name"))
            .filter_type(self.request.query_params.get("type_id"))
            .filter_stock(self.request.query_params.get("min_stock"))
            .apply_sorting(
                self.request.query_params.get("sort_by"),
                self.request.query_params.get("sort_direction"),
            )
        )


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
