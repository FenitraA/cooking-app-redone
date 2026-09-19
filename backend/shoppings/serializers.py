from rest_framework import serializers
from shoppings.models import (
    ItemCategory,
    Shopping,
    ShoppingItem,
    ItemToBuy,
)
class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = "__all__"

class ShoppingItemSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(
        source="ingredient.name",
        read_only=True,
    )

    item_category_name = serializers.CharField(
        source="item_category.name",
        read_only=True,
    )

    class Meta:
        model = ShoppingItem
        fields = "__all__"


class ShoppingSerializer(serializers.ModelSerializer):
    shopping_items = ShoppingItemSerializer(
        many=True,
        read_only=True,
    )

    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Shopping
        fields = "__all__"

    def get_total_cost(self, obj):
        return sum(
            item.unit_price * item.units_bought for item in obj.shopping_items.all()
        )


class ItemToBuySerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(
        source="ingredient.name",
        read_only=True,
    )

    item_category_name = serializers.CharField(
        source="item_category.name",
        read_only=True,
    )

    class Meta:
        model = ItemToBuy
        fields = "__all__"


class ItemCategorySearchSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    
class ItemToBuySearchSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    ingredient_id = serializers.CharField(required=False)
    
class ShoppingItemSearchSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    ingredient_id = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

class ShoppingSearchSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    

### ------------------------------
#  Create serializers
### ------------------------------

class ShoppingCreateFromItemsToBuySerializer(serializers.Serializer):
    item_to_buy_ids = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )

    shopping_date = serializers.DateField()
    description = serializers.CharField()