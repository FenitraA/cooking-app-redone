from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets

from core.views import SoftDeleteModelViewSet
from recipes.models import Meal, Recipe
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
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [DjangoModelPermissions]
    
    
@extend_schema_view(
    list=extend_schema(tags=["Meals"]),
    retrieve=extend_schema(tags=["Meals"]),
    create=extend_schema(tags=["Meals"]),
    update=extend_schema(tags=["Meals"]),
    partial_update=extend_schema(tags=["Meals"]),
    destroy=extend_schema(tags=["Meals"]),
)
class MealViewSet(SoftDeleteModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [DjangoModelPermissions]