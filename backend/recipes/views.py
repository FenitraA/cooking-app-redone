from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets

from core.views import SoftDeleteModelViewSet
from recipes.models import Meal, Recipe
from recipes.querysets.meals import MealQuerySet
from recipes.querysets.recipes import RecipeQuerySet
from recipes.serializers import MealSerializer, RecipeSerializer

@extend_schema_view(
    list=extend_schema(tags=["Recipes"]),
    retrieve=extend_schema(tags=["Recipes"]),
    create=extend_schema(tags=["Recipes"]),
    update=extend_schema(tags=["Recipes"]),
    partial_update=extend_schema(tags=["Recipes"]),
    destroy=extend_schema(tags=["Recipes"]),
)
class RecipeViewSet(SoftDeleteModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self) -> RecipeQuerySet:
        return (
            Recipe.objects
            .active()
            .with_related()
        )
    
    
@extend_schema_view(
    list=extend_schema(tags=["Meals"],parameters=[MealSerializer]),
    retrieve=extend_schema(tags=["Meals"]),
    create=extend_schema(tags=["Meals"]),
    update=extend_schema(tags=["Meals"]),
    partial_update=extend_schema(tags=["Meals"]),
    destroy=extend_schema(tags=["Meals"]),
)
class MealViewSet(SoftDeleteModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self) -> MealQuerySet:
        return (
            Meal.objects
            .active()
            .with_related()
        )