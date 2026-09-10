from rest_framework.routers import DefaultRouter

from .views import (
    UnitGroupViewSet,
    IngredientUnitViewSet,
    IngredientTypeViewSet,
    IngredientViewSet,
    SellerViewSet,
    IngredientStockViewSet,
)

router = DefaultRouter()

router.register("unit-groups", UnitGroupViewSet, basename="unit-group")
router.register("units", IngredientUnitViewSet, basename="ingredient-unit")
router.register("types", IngredientTypeViewSet, basename="ingredient-type")
router.register("", IngredientViewSet, basename="ingredient")
router.register("sellers", SellerViewSet, basename="seller")
router.register("stocks", IngredientStockViewSet, basename="ingredient-stock")

urlpatterns = router.urls
