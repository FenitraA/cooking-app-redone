from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from core.cache_utils import household_cache, clear_household_cache, get_household_id
from plannings.dataclasses import PlanningRecipeRead
from plannings.models import PlanningRecipe
from plannings.querysets.plannings import PlanningRecipeQuerySet
from plannings.serializers import (
    PlanningDateRangeSerializer,
    PlanningRecipeSerializer,
    PlanningResultSerializer,
)
from plannings.services.plannings import (
    build_planning_recipe_reads,
    get_total_estimated_price_from_repartitions,
    get_total_ingredients_to_buy,
    redistribute_to_repartition,
)


@extend_schema_view(
    list=extend_schema(tags=["PlanningRecipes"]),
    retrieve=extend_schema(tags=["PlanningRecipes"]),
    create=extend_schema(tags=["PlanningRecipes"]),
    update=extend_schema(tags=["PlanningRecipes"]),
    partial_update=extend_schema(tags=["PlanningRecipes"]),
    destroy=extend_schema(tags=["PlanningRecipes"]),
)
class PlanningRecipeViewSet(viewsets.ModelViewSet):
    serializer_class = PlanningRecipeSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self) -> PlanningRecipeQuerySet:
        return (
            PlanningRecipe.objects
            .active()
            .with_related()
        )

    @household_cache(namespace="planning_recipes")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @household_cache(namespace="planning_recipes")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        url_path="by-dates",
    )
    @household_cache(namespace="planning_recipes_by_dates")
    @transaction.atomic
    def get_plannings_by_dates(self, request):
        params = PlanningDateRangeSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)

        start_date = params.validated_data["start_date"]
        end_date = params.validated_data["end_date"]

        queryset = (
            PlanningRecipe.objects
            .active()
            .with_related()
            .with_estimated_cost_price()
            .filter_start_date(start_date)
            .filter_end_date(end_date)
        )

        planning_recipe_reads: list[PlanningRecipeRead] = build_planning_recipe_reads(queryset)

        planning_repartitions = redistribute_to_repartition(
            start_of_week=start_date,
            end_of_week=end_date,
            recipes=planning_recipe_reads,
        )

        result = {
            "planning_repartitions": planning_repartitions,
            "total_estimated_cost_price": get_total_estimated_price_from_repartitions(planning_repartitions),
            "ingredients_to_buy": get_total_ingredients_to_buy(planning_repartitions),
        }

        serializer = PlanningResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _invalidate_cache(self):
        household_id = get_household_id(self.request)
        clear_household_cache("planning_recipes", household_id)
        clear_household_cache("planning_recipes_by_dates", household_id)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()