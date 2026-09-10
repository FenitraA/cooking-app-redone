from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
    MealViewSet
)

router = DefaultRouter()

router.register("", RecipeViewSet, basename="recipe")
router.register("meals", MealViewSet, basename="meal")

urlpatterns = router.urls