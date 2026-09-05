from rest_framework import serializers
from ingredients.models import (
    UnitGroup,
    IngredientUnit,
    IngredientType,
    Ingredient,
    Seller,
    IngredientStock,
)

class UnitGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitGroup
        fields = "__all__"
        
class IngredientUnitSerializer(serializers.ModelSerializer):
    unit_group_name = serializers.CharField(
        source="unit_group.name",
        read_only=True,
    )

    class Meta:
        model = IngredientUnit
        fields = "__all__"

class IngredientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientType
        fields = "__all__"
        
class IngredientSerializer(serializers.ModelSerializer):
    ingredient_type_name = serializers.CharField(
        source="ingredient_type.name",
        read_only=True,
    )

    ingredient_unit_name = serializers.CharField(
        source="ingredient_unit.name",
        read_only=True,
    )

    class Meta:
        model = Ingredient
        fields = "__all__"
        
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"
        
class IngredientStockSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(
        source="ingredient.name",
        read_only=True,
    )

    seller_name = serializers.CharField(
        source="seller.name",
        read_only=True,
    )

    class Meta:
        model = IngredientStock
        fields = "__all__"