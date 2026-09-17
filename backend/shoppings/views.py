from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets
from recipes.models import Meal, Recipe
from recipes.serializers import MealSerializer, RecipeSerializer
from shoppings.models import ItemCategory, ItemToBuy, Shopping, ShoppingItem
from shoppings.serializers import (
    ItemCategorySearchSerializer,
    ItemCategorySerializer,
    ItemToBuySearchSerializer,
    ItemToBuySerializer,
    ShoppingItemSearchSerializer,
    ShoppingItemSerializer,
    ShoppingSearchSerializer,
    ShoppingSerializer,
)


@extend_schema_view(
    list=extend_schema(
        tags=["ItemCategories"], parameters=[ItemCategorySearchSerializer]
    ),
    retrieve=extend_schema(tags=["ItemCategories"]),
    create=extend_schema(tags=["ItemCategories"]),
    update=extend_schema(tags=["ItemCategories"]),
    partial_update=extend_schema(tags=["ItemCategories"]),
    destroy=extend_schema(tags=["ItemCategories"]),
)
class ItemCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ItemCategorySerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return ItemCategory.objects.active().filter_name(
            self.request.query_params.get("name")
        )


@extend_schema_view(
    list=extend_schema(tags=["Shoppings"], parameters=[ShoppingSearchSerializer]),
    retrieve=extend_schema(tags=["Shoppings"]),
    create=extend_schema(tags=["Shoppings"]),
    update=extend_schema(tags=["Shoppings"]),
    partial_update=extend_schema(tags=["Shoppings"]),
    destroy=extend_schema(tags=["Shoppings"]),
)
class ShoppingViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return (
            Shopping.objects.active()
            .filter_start_date(self.request.query_params.get("start_date"))
            .filter_end_date(self.request.query_params.get("end_date"))
        )


@extend_schema_view(
    list=extend_schema(tags=["ShoppingItems"], parameters=[ShoppingItemSearchSerializer]),
    retrieve=extend_schema(tags=["ShoppingItems"]),
    create=extend_schema(tags=["ShoppingItems"]),
    update=extend_schema(tags=["ShoppingItems"]),
    partial_update=extend_schema(tags=["ShoppingItems"]),
    destroy=extend_schema(tags=["ShoppingItems"]),
)
class ShoppingItemViewSet(viewsets.ModelViewSet):
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


@extend_schema_view(
    list=extend_schema(tags=["ItemsToBuy"], parameters=[ItemToBuySearchSerializer]),
    retrieve=extend_schema(tags=["ItemsToBuy"]),
    create=extend_schema(tags=["ItemsToBuy"]),
    update=extend_schema(tags=["ItemsToBuy"]),
    partial_update=extend_schema(tags=["ItemsToBuy"]),
    destroy=extend_schema(tags=["ItemsToBuy"]),
)
class ItemToBuyViewSet(viewsets.ModelViewSet):
    serializer_class = ItemToBuySerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return (
            ItemToBuy.objects.active()
            .with_related()
            .filter_name(self.request.query_params.get("name"))
            .filter_ingredient(self.request.query_params.get("ingredient_id"))
        )
