from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets

from core.views import SoftDeleteModelViewSet
from households.models import Household
from households.serializers import HouseholdSerializer


@extend_schema_view(
    list=extend_schema(tags=["Households"]),
    retrieve=extend_schema(tags=["Households"]),
    create=extend_schema(tags=["Households"]),
    update=extend_schema(tags=["Households"]),
    partial_update=extend_schema(tags=["Households"]),
    destroy=extend_schema(tags=["Households"]),
)
class HouseholdViewSet(SoftDeleteModelViewSet):
    serializer_class = HouseholdSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Household.objects.active().filter_name(
            self.request.query_params.get("name")
        )