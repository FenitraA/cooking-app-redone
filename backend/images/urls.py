from django.urls import path
from .views import CloudinarySignView

urlpatterns = [
    path("sign/", CloudinarySignView.as_view(), name="cloudinary"),
]