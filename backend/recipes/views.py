from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from core.views import SoftDeleteModelViewSet
from core.cache_utils import household_cache, clear_household_cache, get_household_id
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

    @household_cache(namespace="recipes")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="recipes")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("recipes", get_household_id(self.request))

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
    list=extend_schema(tags=["Meals"], parameters=[MealSerializer]),
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

    @household_cache(namespace="meals")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="meals")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("meals", get_household_id(self.request))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()