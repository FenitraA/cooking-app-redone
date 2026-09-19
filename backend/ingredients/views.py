from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets

from core.views import SoftDeleteModelViewSet
from ingredients.models import (
    Ingredient,
    IngredientStock,
    IngredientType,
    IngredientUnit,
    Seller,
    UnitGroup,
)

from ingredients.serializers import (
    IngredientSearchSerializer,
    IngredientSerializer,
    IngredientStockSerializer,
    IngredientTypeSearchSerializer,
    IngredientTypeSerializer,
    IngredientUnitSearchSerializer,
    IngredientUnitSerializer,
    SellerSerializer,
    UnitGroupSerializer,
)
import cloudinary.uploader

@extend_schema_view(
    list=extend_schema(tags=["UnitGroups"]),
    retrieve=extend_schema(tags=["UnitGroups"]),
    create=extend_schema(tags=["UnitGroups"]),
    update=extend_schema(tags=["UnitGroups"]),
    partial_update=extend_schema(tags=["UnitGroups"]),
    destroy=extend_schema(tags=["UnitGroups"]),
)
class UnitGroupViewSet(SoftDeleteModelViewSet):
    queryset = UnitGroup.objects.all()
    serializer_class = UnitGroupSerializer
    permission_classes = [DjangoModelPermissions]


@extend_schema_view(
    list=extend_schema(
        tags=["IngredientUnits"], parameters=[IngredientUnitSearchSerializer]
    ),
    retrieve=extend_schema(tags=["IngredientUnits"]),
    create=extend_schema(tags=["IngredientUnits"]),
    update=extend_schema(tags=["IngredientUnits"]),
    partial_update=extend_schema(tags=["IngredientUnits"]),
    destroy=extend_schema(tags=["IngredientUnits"]),
)
class IngredientUnitViewSet(SoftDeleteModelViewSet):
    serializer_class = IngredientUnitSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return IngredientUnit.objects.active().filter_name(
            self.request.query_params.get("name")
        )


@extend_schema_view(
    list=extend_schema(
        tags=["IngredientTypes"], parameters=[IngredientTypeSearchSerializer]
    ),
    retrieve=extend_schema(tags=["IngredientTypes"]),
    create=extend_schema(tags=["IngredientTypes"]),
    update=extend_schema(tags=["IngredientTypes"]),
    partial_update=extend_schema(tags=["IngredientTypes"]),
    destroy=extend_schema(tags=["IngredientTypes"]),
)
class IngredientTypeViewSet(SoftDeleteModelViewSet):
    serializer_class = IngredientTypeSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return IngredientType.objects.active().filter_name(
            self.request.query_params.get("name")
        )


@extend_schema_view(
    list=extend_schema(tags=["Ingredients"], parameters=[IngredientSearchSerializer]),
    retrieve=extend_schema(tags=["Ingredients"]),
    create=extend_schema(tags=["Ingredients"]),
    update=extend_schema(tags=["Ingredients"]),
    partial_update=extend_schema(tags=["Ingredients"]),
    destroy=extend_schema(tags=["Ingredients"]),
)
class IngredientViewSet(SoftDeleteModelViewSet):
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

    def perform_update(self, serializer):
        ingredient = self.get_object()

        old_storage_key = ingredient.storage_key

        super().perform_update(serializer)

        new_storage_key = ingredient.storage_key

        if old_storage_key and old_storage_key != new_storage_key:
            cloudinary.uploader.destroy(
                old_storage_key,
                invalidate=True,
            )


@extend_schema_view(
    list=extend_schema(tags=["Sellers"], parameters=[SellerSerializer]),
    retrieve=extend_schema(tags=["Sellers"]),
    create=extend_schema(tags=["Sellers"]),
    update=extend_schema(tags=["Sellers"]),
    partial_update=extend_schema(tags=["Sellers"]),
    destroy=extend_schema(tags=["Sellers"]),
)
class SellerViewSet(SoftDeleteModelViewSet):
    serializer_class = SellerSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Seller.objects.active().filter_name(
            self.request.query_params.get("name")
        )


@extend_schema_view(
    list=extend_schema(tags=["IngredientStocks"], parameters=[IngredientStockSerializer]),
    retrieve=extend_schema(tags=["IngredientStocks"]),
    create=extend_schema(tags=["IngredientStocks"]),
    update=extend_schema(tags=["IngredientStocks"]),
    partial_update=extend_schema(tags=["IngredientStocks"]),
    destroy=extend_schema(tags=["IngredientStocks"]),
)
class IngredientStockViewSet(SoftDeleteModelViewSet):
    queryset = IngredientStock.objects.all()
    serializer_class = IngredientStockSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return IngredientStock.objects.active().filter_ingredient(
            self.request.query_params.get("ingredient_id")
        )
