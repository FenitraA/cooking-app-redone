from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets
from recipes.models import Meal, Recipe
from recipes.serializers import MealSerializer, RecipeSerializer
from shoppings.models import ItemCategory, ItemToBuy, Shopping, ShoppingItem
from shoppings.serializers import (
    ItemCategorySerializer,
    ItemToBuySerializer,
    ShoppingItemSerializer,
    ShoppingSerializer,
)

@extend_schema_view(
    list=extend_schema(tags=["ItemCategories"]),
    retrieve=extend_schema(tags=["ItemCategories"]),
    create=extend_schema(tags=["ItemCategories"]),
    update=extend_schema(tags=["ItemCategories"]),
    partial_update=extend_schema(tags=["ItemCategories"]),
    destroy=extend_schema(tags=["ItemCategories"]),
)
class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer
    permission_classes = [DjangoModelPermissions]


@extend_schema_view(
    list=extend_schema(tags=["Shoppings"]),
    retrieve=extend_schema(tags=["Shoppings"]),
    create=extend_schema(tags=["Shoppings"]),
    update=extend_schema(tags=["Shoppings"]),
    partial_update=extend_schema(tags=["Shoppings"]),
    destroy=extend_schema(tags=["Shoppings"]),
)
class ShoppingViewSet(viewsets.ModelViewSet):
    queryset = Shopping.objects.all()
    serializer_class = ShoppingSerializer
    permission_classes = [DjangoModelPermissions]


@extend_schema_view(
    list=extend_schema(tags=["ShoppingItems"]),
    retrieve=extend_schema(tags=["ShoppingItems"]),
    create=extend_schema(tags=["ShoppingItems"]),
    update=extend_schema(tags=["ShoppingItems"]),
    partial_update=extend_schema(tags=["ShoppingItems"]),
    destroy=extend_schema(tags=["ShoppingItems"]),
)
class ShoppingItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    permission_classes = [DjangoModelPermissions]


@extend_schema_view(
    list=extend_schema(tags=["ItemsToBuy"]),
    retrieve=extend_schema(tags=["ItemsToBuy"]),
    create=extend_schema(tags=["ItemsToBuy"]),
    update=extend_schema(tags=["ItemsToBuy"]),
    partial_update=extend_schema(tags=["ItemsToBuy"]),
    destroy=extend_schema(tags=["ItemsToBuy"]),
)
class ItemToBuyViewSet(viewsets.ModelViewSet):
    queryset = ItemToBuy.objects.all()
    serializer_class = ItemToBuySerializer
    permission_classes = [DjangoModelPermissions]

