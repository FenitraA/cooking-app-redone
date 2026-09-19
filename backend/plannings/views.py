from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets

from core.views import SoftDeleteModelViewSet
from plannings.models import PlanningRecipe
from plannings.serializers import PlanningRecipeSerializer

@extend_schema_view(
    list=extend_schema(tags=["PlanningRecipes"]),
    retrieve=extend_schema(tags=["PlanningRecipes"]),
    create=extend_schema(tags=["PlanningRecipes"]),
    update=extend_schema(tags=["PlanningRecipes"]),
    partial_update=extend_schema(tags=["PlanningRecipes"]),
    destroy=extend_schema(tags=["PlanningRecipes"]),
)
class PlanningRecipeViewSet(SoftDeleteModelViewSet):
    queryset = PlanningRecipe.objects.all()
    serializer_class = PlanningRecipeSerializer
    permission_classes = [DjangoModelPermissions]