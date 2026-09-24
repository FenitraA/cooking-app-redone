from rest_framework import serializers
from plannings.models import PlanningRecipe
from recipes.serializers import RecipeSerializer, RecipeIngredientSerializer, RecipeIngredientReadSerializer


class PlanningRecipeSerializer(serializers.ModelSerializer):
    recipe_name = serializers.CharField(
        source="recipe.name",
        read_only=True,
    )

    class Meta:
        model = PlanningRecipe
        fields = "__all__"

class PlanningRecipeReadSerializer(serializers.Serializer):
    planning_recipe = PlanningRecipeSerializer()
    recipe = RecipeSerializer()
    estimated_cost_price = serializers.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
    recipe_ingredients = RecipeIngredientReadSerializer(
        many=True
    )

class PlanningRepartitionSerializer(serializers.Serializer):
    planning_group_date = serializers.DateField()
    day_name = serializers.CharField()
    planning_recipes = PlanningRecipeReadSerializer(
        many=True
    )
    estimated_cost_price = serializers.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
class PlanningResultSerializer(serializers.Serializer):
    planning_partitions = PlanningRepartitionSerializer(
        many=True
    )

    total_estimated_cost_price = serializers.DecimalField(
        max_digits=16,
        decimal_places=2,
    )

    ingredients_to_buy = RecipeIngredientSerializer(
        many=True
    )


### ------------------------------
#  Search serializers
### ------------------------------

class PlanningDateRangeSerializer(
    serializers.Serializer
):
    start_date = serializers.DateField()
    end_date = serializers.DateField()