from rest_framework.routers import DefaultRouter

from .views import (
    ItemCategoryViewSet,
    ShoppingItemViewSet,
    ShoppingViewSet,
    ItemToBuyViewSet
)

router = DefaultRouter()

router.register("item-categories", ItemCategoryViewSet, basename="item-category")
router.register("shopping-items", ShoppingItemViewSet, basename="shopping-item")
router.register("", ShoppingViewSet, basename="shopping")
router.register("items-to-buy", ItemToBuyViewSet, basename="item-to-buy")

urlpatterns = router.urls