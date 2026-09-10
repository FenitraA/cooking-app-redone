from rest_framework.routers import DefaultRouter

from .views import (
    PlanningRecipeViewSet
)

router = DefaultRouter()

router.register("", PlanningRecipeViewSet, basename="planning-recipe")

urlpatterns = router.urls