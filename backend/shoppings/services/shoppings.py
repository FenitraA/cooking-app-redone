from shoppings.models import ItemToBuy, Shopping, ShoppingItem


class ShoppingService:

    @staticmethod
    def create_from_items_to_buy(
            household,
            data,
    ):
        item_to_buy_ids = data["item_to_buy_ids"]

        items_to_buy = list(
            ItemToBuy.objects.active().filter(
                id__in=item_to_buy_ids,
                household=household,
            )
        )

        # Create Shopping
        shopping = Shopping.objects.create(
            household=household,
            description=data["description"],
            shopping_date=data["shopping_date"],
        )

        # Create ShoppingItems
        shopping_items = [
            ShoppingItem(
                shopping=shopping,
                name=item.name,
                description=item.description,
                unit_price=item.estimated_unit_price,
                units_bought=item.units_to_buy,
                ingredient=item.ingredient,
                item_category=item.item_category,
            )
            for item in items_to_buy
        ]

        new_shopping_items = ShoppingItem.objects.bulk_create(shopping_items)

        # Mark ItemToBuy as bought
        for item_to_buy, shopping_item in zip(
                items_to_buy,
                new_shopping_items,
                strict=True,
        ):
            item_to_buy.ref_shopping_item_id = shopping_item.id
            item_to_buy.state = 10

        ItemToBuy.objects.bulk_update(
            items_to_buy,
            [
                "ref_shopping_item",
                "state",
                "updated_at",
            ],
        )

        return shopping
