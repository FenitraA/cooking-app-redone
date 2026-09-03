from django.urls import path
from .views import HouseholdView

urlpatterns = [
    path("", HouseholdView.as_view(), name="household"),
]