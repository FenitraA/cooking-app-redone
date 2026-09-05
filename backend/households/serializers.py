from rest_framework import serializers
from households.models import Household

class HouseholdQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False)
    search = serializers.CharField(required=False)


class HouseholdCreateSerializer(serializers.Serializer):
    name = serializers.CharField()

class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = "__all__"