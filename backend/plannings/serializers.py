from rest_framework import serializers
from plannings.models import PlanningRecipe


class PlanningRecipeSerializer(serializers.ModelSerializer):
    recipe_name = serializers.CharField(
        source="recipe.name",
        read_only=True,
    )

    class Meta:
        model = PlanningRecipe
        fields = "__all__"