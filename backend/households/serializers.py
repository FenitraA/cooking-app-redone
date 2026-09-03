from rest_framework import serializers


class HouseholdQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False)
    search = serializers.CharField(required=False)


class HouseholdCreateSerializer(serializers.Serializer):
    name = serializers.CharField()