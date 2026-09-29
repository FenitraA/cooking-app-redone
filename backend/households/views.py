from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets

from core.cache_utils import household_cache, clear_household_cache, get_household_id
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

    @household_cache(namespace="households")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="households")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _invalidate_cache(self):
        clear_household_cache("households", get_household_id(self.request))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()