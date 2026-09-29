from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from core.views import SoftDeleteModelViewSet
from core.cache_utils import household_cache, clear_household_cache, get_household_id
from shoppings.models import ItemCategory, ItemToBuy, Shopping, ShoppingItem
from shoppings.serializers import (
    ItemCategorySearchSerializer,
    ItemCategorySerializer,
    ItemToBuySearchSerializer,
    ItemToBuySerializer,
    ShoppingCreateFromItemsToBuySerializer,
    ShoppingItemSearchSerializer,
    ShoppingItemSerializer,
    ShoppingSearchSerializer,
    ShoppingSerializer,
)
from shoppings.services.shoppings import ShoppingService


@extend_schema_view(
    list=extend_schema(tags=["ItemCategories"], parameters=[ItemCategorySearchSerializer]),
    retrieve=extend_schema(tags=["ItemCategories"]),
    create=extend_schema(tags=["ItemCategories"]),
    update=extend_schema(tags=["ItemCategories"]),
    partial_update=extend_schema(tags=["ItemCategories"]),
    destroy=extend_schema(tags=["ItemCategories"]),
)
class ItemCategoryViewSet(SoftDeleteModelViewSet):
    serializer_class = ItemCategorySerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return ItemCategory.objects.active().filter_name(
            self.request.query_params.get("name")
        )

    @household_cache(namespace="item_categories")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="item_categories")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("item_categories", get_household_id(self.request))

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
    list=extend_schema(tags=["Shopping"], parameters=[ShoppingSearchSerializer]),
    retrieve=extend_schema(tags=["Shopping"]),
    create=extend_schema(tags=["Shopping"]),
    update=extend_schema(tags=["Shopping"]),
    partial_update=extend_schema(tags=["Shopping"]),
    destroy=extend_schema(tags=["Shopping"]),
)
class ShoppingViewSet(SoftDeleteModelViewSet):
    serializer_class = ShoppingSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return (
            Shopping.objects.active()
            .filter_start_date(self.request.query_params.get("start_date"))
            .filter_end_date(self.request.query_params.get("end_date"))
        )

    @household_cache(namespace="shoppings")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="shoppings")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["post"],
        url_path="from-items-to-buy",
    )
    @transaction.atomic
    def create_from_items_to_buy(self, request):
        serializer = ShoppingCreateFromItemsToBuySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shopping = ShoppingService.create_from_items_to_buy(
            household=request.user.household,
            data=serializer.validated_data,
        )

        household_id = get_household_id(request)
        clear_household_cache("shoppings", household_id)
        clear_household_cache("items_to_buy", household_id)

        return Response(
            ShoppingSerializer(shopping).data,
            status=status.HTTP_201_CREATED,
        )

    def _invalidate_cache(self):
        clear_household_cache("shoppings", get_household_id(self.request))

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
    list=extend_schema(tags=["ShoppingItems"], parameters=[ShoppingItemSearchSerializer]),
    retrieve=extend_schema(tags=["ShoppingItems"]),
    create=extend_schema(tags=["ShoppingItems"]),
    update=extend_schema(tags=["ShoppingItems"]),
    partial_update=extend_schema(tags=["ShoppingItems"]),
    destroy=extend_schema(tags=["ShoppingItems"]),
)
class ShoppingItemViewSet(SoftDeleteModelViewSet):
    serializer_class = ShoppingItemSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return (
            ShoppingItem.objects.active()
            .with_related()
            .filter_name(self.request.query_params.get("name"))
            .filter_ingredient(self.request.query_params.get("ingredient_id"))
            .filter_start_date(self.request.query_params.get("start_date"))
            .filter_end_date(self.request.query_params.get("end_date"))
        )

    @household_cache(namespace="shopping_items")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="shopping_items")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("shopping_items", get_household_id(self.request))

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
    list=extend_schema(tags=["ItemsToBuy"], parameters=[ItemToBuySearchSerializer]),
    retrieve=extend_schema(tags=["ItemsToBuy"]),
    create=extend_schema(tags=["ItemsToBuy"]),
    update=extend_schema(tags=["ItemsToBuy"]),
    partial_update=extend_schema(tags=["ItemsToBuy"]),
    destroy=extend_schema(tags=["ItemsToBuy"]),
)
class ItemToBuyViewSet(SoftDeleteModelViewSet):
    serializer_class = ItemToBuySerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return (
            ItemToBuy.objects.active()
            .with_related()
            .filter_name(self.request.query_params.get("name"))
            .filter_ingredient(self.request.query_params.get("ingredient_id"))
        )

    @household_cache(namespace="items_to_buy")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="items_to_buy")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("items_to_buy", get_household_id(self.request))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()