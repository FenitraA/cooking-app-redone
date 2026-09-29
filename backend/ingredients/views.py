import cloudinary.uploader
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions

from core.views import SoftDeleteModelViewSet
from core.cache_utils import household_cache, clear_household_cache, get_household_id
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

    @household_cache(namespace="unit_groups")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="unit_groups")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("unit_groups", get_household_id(self.request))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()


@extend_schema_view(
    list=extend_schema(tags=["IngredientUnits"], parameters=[IngredientUnitSearchSerializer]),
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

    @household_cache(namespace="ingredient_units")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="ingredient_units")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("ingredient_units", get_household_id(self.request))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()


@extend_schema_view(
    list=extend_schema(tags=["IngredientTypes"], parameters=[IngredientTypeSearchSerializer]),
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

    @household_cache(namespace="ingredient_types")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="ingredient_types")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("ingredient_types", get_household_id(self.request))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()


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

    @household_cache(namespace="ingredients")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="ingredients")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("ingredients", get_household_id(self.request))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

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

        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()


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

    @household_cache(namespace="sellers")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="sellers")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("sellers", get_household_id(self.request))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()


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

    @household_cache(namespace="ingredient_stocks")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="ingredient_stocks")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        household_id = get_household_id(self.request)
        clear_household_cache("ingredient_stocks", household_id)
        # Stock updates recalculate ingredient quantities, so clear ingredients cache as well
        clear_household_cache("ingredients", household_id)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()