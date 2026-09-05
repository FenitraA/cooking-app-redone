from rest_framework import serializers
from recipes.models import (
    Recipe,
    RecipeIngredient,
    Meal,
    MealIngredient,
)

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(
        source="ingredient.name",
        read_only=True,
    )

    ingredient_unit = serializers.CharField(
        source="ingredient.ingredient_unit.symbol",
        read_only=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = "__all__"
        
class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = "__all__"
        
class MealIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(
        source="ingredient_stock.ingredient.name",
        read_only=True,
    )

    seller_name = serializers.CharField(
        source="ingredient_stock.seller.name",
        read_only=True,
    )

    class Meta:
        model = MealIngredient
        fields = "__all__"
        
class MealSerializer(serializers.ModelSerializer):
    meal_ingredients = MealIngredientSerializer(
        many=True,
        read_only=True,
    )

    recipe_name = serializers.CharField(
        source="recipe.name",
        read_only=True,
    )

    class Meta:
        model = Meal
        fields = "__all__"