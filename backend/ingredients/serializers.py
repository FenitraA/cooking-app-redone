from decimal import Decimal

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

    quantity_left = serializers.DecimalField(
        max_digits=16,
        decimal_places=2,
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


### ------------------------------
#  Search serializers
### ------------------------------


class IngredientSearchSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)

    type_id = serializers.CharField(required=False)

    min_stock = serializers.DecimalField(
        max_digits=16,
        decimal_places=2,
        required=False,
    )

    sort_by = serializers.ChoiceField(
        choices=[
            "unit_cost",
            "quantity_left",
        ],
        required=False,
    )

    sort_direction = serializers.ChoiceField(
        choices=[
            "asc",
            "desc",
        ],
        required=False,
    )

class IngredientTypeSearchSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    
class IngredientUnitSearchSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)

class IngredientStockSearchSerializer(serializers.Serializer):
    ingredient_id = serializers.CharField(required=False)
    
class SellerSearchSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)

