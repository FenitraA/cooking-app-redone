from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from households.serializers import HouseholdCreateSerializer, HouseholdQuerySerializer


class HouseholdView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[HouseholdQuerySerializer],
        responses=HouseholdQuerySerializer,
    )
    def get(self, request):
        serializer = HouseholdQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)

    @extend_schema(
        request=HouseholdCreateSerializer,
        responses=HouseholdCreateSerializer,
    )
    def post(self, request):
        serializer = HouseholdCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)
